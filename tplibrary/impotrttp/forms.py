from django import forms
from .models import AddTP

class AddTPForm(forms.ModelForm):
    class Meta:
        model = AddTP
        fields = ['author', 'title', 'description']