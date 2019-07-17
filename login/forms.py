from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.forms import ModelForm
from django import forms

class SignUpForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Enter E-Mail'}))
    first_name = forms.CharField(required=False,widget=forms.TextInput(attrs={'placeholder': 'Enter First Name'}))
    last_name = forms.CharField(required=False,widget=forms.TextInput(attrs={'placeholder': 'Enter Last Name'}))
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

class SignInForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}))
    class Meta:
        model = User
        fields = ('username', 'password')

class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Old Password'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter New Password'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter New Password'}))
    class Meta:
        model = User
        fields = '__all__'

class forgotpw(ModelForm):
	email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Username'}))
	class Meta:
		model = User
		fields = ['email']
