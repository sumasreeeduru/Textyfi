from django import forms
from .models import handwritten
class handwrittenForm(forms.ModelForm):
    class Meta:
        model=handwritten
        fields=['textfile']