from django import forms
from .models import *


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control mb-3",
                                                             "placeholder": "Enter your username"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control mb-3",
                                                                 "placeholder": "Enter your password"}))


class SignUpForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control mb-3",
                                                             "placeholder": "dr_pepper"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control mb-3",
                                                            "placeholder": "dr.pepper@mail.ru"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control mb-3",
                                                                 "placeholder": "Enter your password"}))
    password_repeat = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control mb-3",
                                                                        "placeholder": "Enter your password again"}))

    avatar = forms.ImageField(required=False, widget=forms.FileInput(attrs={"class": "form-control mb-3"}))

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_repeat = cleaned_data.get("password_repeat")

        if password != password_repeat:
            self.add_error(None, "Passwords do not match!")

        p = list(User.objects.values_list("username", flat=True))
        username = cleaned_data.get("username")

        if username in p:
            self.add_error(None, "This username is already used!")

        e = list(User.objects.values_list("email", flat=True))
        email = cleaned_data.get("email")

        if email in e:
            self.add_error(None, "This email is already used!")

    def save(self):
        user = User.objects.create(username=self.cleaned_data.get("username"),
                                   email=self.cleaned_data.get("email"))
        user.set_password(self.cleaned_data.get("password"))
        user.save()
        Profile.objects.create(user=user, login=user.username)
        return user


class SettingsForm(forms.Form):
    username = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control mb-3",
                                                                             "placeholder": "dr_pepper"}))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={"class": "form-control mb-3",
                                                                            "placeholder": "dr.pepper@mail.ru"}))
    old_password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={"class": "form-control mb-3",
                                                                                     "placeholder": "Enter your old password"}))
    password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={"class": "form-control mb-3",
                                                                                 "placeholder": "Enter your new password"}))
    password_repeat = forms.CharField(required=False, widget=forms.PasswordInput(attrs={"class": "form-control mb-3",
                                                                                        "placeholder": "Enter your new password again"}))
    avatar = forms.ImageField(required=False, widget=forms.FileInput(attrs={"class": "form-control mb-3"}))


class AskForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control mb-3",
                                                          "placeholder": "Enter your question"}))
    text = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control mb-3",
                                                        "placeholder": "Describe your question", "rows": 10}))
    tags = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control mb-3",
                                                         "placeholder": "Add tags (e.g. Bootstrap, Django, Python)"}))

    def save(self):
        tags = []
        for tag in self.cleaned_data["tags"].split(','):
            tags.append(tag.strip())
        tag_list = []
        for tag in tags:
            t = Tag.objects.filter(tag_name=tag).first()
            if not t:
                t = Tag.objects.create(tag_name=tag)
            tag_list.append(t)
        return tag_list


class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control mb-3",
                                                        "placeholder": "Enter your answer", "rows": 7}), label="Your answer:")
