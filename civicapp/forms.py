from django import forms
from .models import *


class IssueForm(forms.ModelForm):

    class Meta:
        model = Issue

        fields = [
            'title',
            'description',
            'category',
            'county',
            'sub_county',
            'ward',
            'image'
        ]

        widgets = {

            'title': forms.TextInput(
                attrs={
                    'placeholder': 'Example: Broken bridge near market'
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'placeholder': 'Describe the problem clearly...'
                }
            ),

            'county': forms.TextInput(
                attrs={
                    'placeholder': 'Example: Siaya County'
                }
            ),

            'sub_county': forms.TextInput(
                attrs={
                    'placeholder': 'Example: Ugenya'
                }
            ),

            'ward': forms.TextInput(
                attrs={
                    'placeholder': 'Example: Ukwala Ward'
                }
            ),

        }



class ProfileImageForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['profile_image']