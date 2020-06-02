from django import forms
from django.forms import ModelForm, TextInput, EmailInput
from django.forms.utils import ErrorList
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS

from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm

class SearchForm(forms.Form):
    product_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Rechercher'}),
        required=True
    )

class UserCreateForm(UserCreationForm):
    first_name= forms.CharField(
        label='Nom',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}),
        required=True
    )

    email= forms.EmailField(
        label='Email',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        required=True
    )

    password1 = forms.CharField(
        label="Mot de passe",
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'}),
        required=True
    )

    password2 = forms.CharField(
        label="Confirmation mot de passe",
        strip=False,
        help_text="Enter the same password as before, for verification.",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Vérification mot de passe'}),
        required=True
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "email", "password1", "password2"]
        widgets = {
            'username': TextInput(attrs={'class': 'form-control', 'placeholder': 'Identifiant'})
        }

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email__iexact=email).exists(): # check if email exists
            raise ValidationError("Un utilisateur avec l'email %(email)s existe déjà.", code='email', params={'email': email})

        return email

class LoginForm(AuthenticationForm):    
    username = UsernameField(
        label='Identifiant',
        widget=forms.TextInput(attrs={'autofocus': False, 'class': 'form-control', 'placeholder': 'Identifiant'}),
        required=True
    )

    password = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'}),
        required=True
    )

    class Meta:
        model = User
        fields = ('username', 'password')
