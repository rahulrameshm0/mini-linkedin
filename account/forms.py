from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class SignupForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('An account already uses this email address.')
        return email

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('headline', 'location', 'bio')


class DeleteAccountForm(forms.Form):
    password = forms.CharField(label='Current password', widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}))
    confirm = forms.BooleanField(label='I understand that deleting my account is permanent.')

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_password(self):
        password = self.cleaned_data['password']
        if not self.user.check_password(password):
            raise forms.ValidationError('Your password is incorrect.')
        return password
