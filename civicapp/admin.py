from django.contrib import admin
from .models import *

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'location', 'created_by', 'created_at')
    list_filter = ('status', 'category')
    search_fields = ('title', 'description', 'location')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)
    search_fields = ('user__username',)