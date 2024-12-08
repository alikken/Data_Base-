from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, label="Логин", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=128, label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
