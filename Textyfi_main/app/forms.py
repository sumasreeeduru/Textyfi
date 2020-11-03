from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import user_model
from django.contrib.auth import authenticate
from api.models import wordcounterModel

class user_model_Form(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = user_model
        fields = ['email', 'username', 'firstname', 'lastname', 'dob', 'password1', 'password2']


class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = user_model
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid login")

class ReviewForm(forms.ModelForm):
    review= forms.CharField(label='Review')
    class Meta:
        fields=('review',)


