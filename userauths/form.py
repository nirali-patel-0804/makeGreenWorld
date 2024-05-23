from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User

class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"First name","class":"form-control"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Last name","class":"form-control"}))
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Username","class":"form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder":"E-mail","class":"form-control"}))
    phone = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Phone no.","class":"form-control"}))
    address = forms.CharField(widget=forms.Textarea(attrs={"placeholder":"Address","class":"form-control"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Password","class":"form-control"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Confirm Passord","class":"form-control"}))
    
    class Meta:
        model=User
        fields=['first_name','last_name','username','email','phone','address','password1','password2']
        