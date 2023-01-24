from django import forms


class CreateUserForm(forms.Form):
    username = forms.CharField(label="Username", max_length=150,)
    password1 = forms.CharField(label="Password", max_length=150, widget=forms.PasswordInput,)
    password2 = forms.CharField(label="Password confirmation", max_length=150, widget=forms.PasswordInput,)


class EditUserProfileForm(forms.Form):
    first_name = forms.CharField(label="first_name", max_length=150,)
    last_name = forms.CharField(label="last_name", max_length=150,)
    about_me = forms.CharField(label="about_me", widget=forms.Textarea, max_length=1000,)