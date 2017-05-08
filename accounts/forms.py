from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms

from accounts.models import *


class UserCreateForm(UserCreationForm):
    class Meta:
        fields = ("username", "email", "password1", "password2")
        model = User

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields["username"].label = "Display name"
            self.fields["email"].label = "Email Address"
            self.fields["password1"].label = "Password"
            self.fields["password2"].label = "Confirm Password"


