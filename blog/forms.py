from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from blog.models import Author, Post, Comment


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ("title", "title_tag", "authors", "body", "category", "snippet", "post_image")

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "title_tag": forms.TextInput(attrs={"class": "form-control"}),
            "authors": forms.TextInput(attrs={"class": "form-control", "value": "", "id": "elder", "type": "hidden"}),
            "body": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.SelectMultiple(attrs={"class": "form-control"}),
            "snippet": forms.TextInput(attrs={"class": "form-control"}),
        }


class RegisterUserForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter username",
                "class": "form-control"
            }
        ))

    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter your first name",
                "class": "form-control"
            }
        ))

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter you last name",
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Enter e-mail",
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Enter password",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Enter password again",
                "class": "form-control"
            }
        ))

    def clean_password1(self):
        password1 = self.cleaned_data["password1"]
        if password1:
            password_validation.validate_password(password1)
        return password1

    def clean(self):
        super().clean()
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            errors = {"password2": ValidationError(
                "The entered passwords do not match",
                code="password_mismatch")}
            raise ValidationError(errors)
        else:
            return self.cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = True
        user.is_activated = True
        if commit:
            user.save()
        return user

    class Meta:
        model = Author
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2",
                  )


class RegisterEditUserForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter username",
                "class": "form-control"
            }
        ))

    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter your first name",
                "class": "form-control"
            }
        ))

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter you last name",
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Enter e-mail",
                "class": "form-control"
            }
        ))

    bio = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter your biography",
                "class": "form-control"
            }
        ))

    date_of_birth = forms.DateField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        ))

    facebook_url = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter your facebook url",
                "class": "form-control"
            }
        ))

    twitter_url = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter your twitter url",
                "class": "form-control"
            }
        ))

    instagram_url = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter your instagram url",
                "class": "form-control"
            }
        ))

    class Meta:
        model = Author
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "bio",
                  "date_of_birth",
                  "avatar",
                  "facebook_url",
                  "twitter_url",
                  "instagram_url",
                  )


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("name", "body")

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "body": forms.Textarea(attrs={"class": "form-control"}),
        }
