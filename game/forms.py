from django import forms



class CreateUserForm(forms.Form):
    username = forms.CharField(label="Username", max_length=150,)
    password1 = forms.CharField(label="Password", max_length=150, widget=forms.PasswordInput,)
    password2 = forms.CharField(label="Password confirmation", max_length=150, widget=forms.PasswordInput,)
