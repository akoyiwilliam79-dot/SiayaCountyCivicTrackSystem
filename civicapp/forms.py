from django import forms
from .models import Issue

class IssueForm(forms.ModelForm):

    class Meta:
        model = Issue
        fields = [
            'title',
            'description',
            'category',
            'location',
            'image'
        ]

        widgets = {

            'title': forms.TextInput(
                attrs={
                    'placeholder':'Example: Broken bridge near market'
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'placeholder':'Describe the problem clearly...'
                }
            ),

            'location': forms.TextInput(
                attrs={
                    'placeholder':'Example: Ugenya Ward, Siaya'
                }
            ),

        }