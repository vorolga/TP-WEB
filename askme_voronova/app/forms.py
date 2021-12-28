from django import forms
from django.core import validators
from django.forms import CharField


class SlugField(CharField):
    def validate(self, value):
        value = super().validate()
        if value ==


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
