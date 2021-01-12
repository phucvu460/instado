from django import forms
from .models import Comment, Post


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'caption']

        labels = {
            'caption': ''
        }

        widgets = {
            'caption': forms.Textarea(attrs={
                'placeholder': 'What do you think?',
                'class': 'mt-2'
            })
        }
