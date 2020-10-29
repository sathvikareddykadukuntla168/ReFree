'''from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User
from phonenumber_field.modelfields import PhoneNumberField

class Signupform(UserCreationForm):
    username = forms.CharField()
    first_name = forms.CharField(max_length=32, help_text='First name')
    last_name=forms.CharField(max_length=32, help_text='Last name')
    email=forms.EmailField(max_length=64, help_text='Enter a valid email address')
    phonenumber = PhoneNumberField()
    password1=forms.CharField()
    password2=forms.CharField()

    class Meta(UserCreationForm.Meta):
        model = User
        # I've tried both of these 'fields' declaration, result is the same
        # fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email',)'''