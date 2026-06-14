
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class Issue(models.Model):
    CATEGORY_CHOICES = [
        ('roads', 'Roads'),
        ('water', 'Water'),
        ('health', 'Health'),
        ('education', 'Education'),
        ('security', 'Security'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    location = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    image = models.ImageField(upload_to='issues/', blank=True, null=True)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    


class Profile(models.Model):

    ROLE_CHOICES = [
        ('citizen', 'Citizen'),
        ('officer', 'Officer'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='citizen')

    def __str__(self):
        return self.user.username
    

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):

    if created:
        Profile.objects.create(user=instance)

class IssueLog(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='logs')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.issue.title} - {self.created_at}"
    
class Vote(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    issue = models.ForeignKey(
        Issue,
        on_delete=models.CASCADE,
        related_name='votes'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ['user', 'issue']