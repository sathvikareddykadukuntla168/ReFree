from django import forms
from phonenumber_field.modelfields import PhoneNumberField

class Signupform(forms.Form):
    username = forms.CharField(label='Your name', max_length=100)
    firstname =forms.CharField(max_length= 50)
    lastname =forms.CharField(max_length= 50)
    email = forms.EmailField(max_length=254)
    phone_number=PhoneNumberField()
    password =forms.CharField(max_length= 50)
    confirmpassword =forms.CharField(max_length= 50)