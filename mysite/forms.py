from django import forms
from .models import TheBlog


class BlogForms(forms.ModelForm):
    class Meta:
        model = TheBlog
        fields = [
            'title',
            'content',
        ]
        