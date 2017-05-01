from django import forms
from django.forms import ModelForm
from django.forms import Textarea
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import password_validation

from webblog.models import BlogUser


class NewPost(forms.Form):
    title = forms.CharField(max_length=100,widget=forms.TextInput(
        attrs={
            'placeholder':"Post title",
            'class':'form-control'
            }))
    content = forms.CharField(widget=Textarea(
        attrs={
            'placeholder':"Post Content",
            'class':'form-control',
            'rows':'10',
            'vertical-align':'top'
            }))
    tags = forms.CharField(max_length=100,widget=forms.TextInput(
        attrs={
            'placeholder':"Tag",
            'class':'form-control'
            }),
        required=False)

class AddComment(forms.Form):
    # author_email = forms.EmailField(max_length=300)
    cccontent = forms.CharField(label='', widget=forms.Textarea(
        attrs={
            'placeholder':'Your comment Here',
            'vertical-align':'top',
            'class':'form-control',
            'rows':'3'
        }
    ))
    form = forms.CharField(max_length=15, widget=forms.TextInput(
    attrs={
        'name':'form_name',
        'value':'addcomment',
        'type':'hidden'
    }
    ))

class AddTag(forms.Form):
    name = forms.CharField(max_length=100, label='', widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'placeholder':'Your tag here.',
        }))

    form = forms.CharField(max_length=10,widget=forms.TextInput(
    attrs={
    'name':'form_name',
    'value':'addtag',
    'type':'hidden'}))

class AddContent(forms.Form):
    ccontent = forms.CharField(label='', widget=Textarea(
        attrs={
            'placeholder':'Add content here to extend the BlogPost',
            'class':'form-control',
            'vertical-align':'top',
            'rows':'5'
        }
    ))
    form = forms.CharField(widget=forms.TextInput(
        attrs={
            'name':'form_name',
            'value': 'addcontent',
            'type' : 'hidden',
            'class':'form-control'
        }
    ))


class RegisterUserForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
    }

    email = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder':'Your email here',
            'class':'form-control'
            }))
    password1 = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
            'placeholder':'Your password here',
            'class':'form-control'
            })
        # help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=("Password confirmation"),
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Password Confirmation',
                'class':'form-control'
                }),
        strip=False,
        # help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = BlogUser
        fields = ("email",)

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs.update({'autofocus': True})

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        self.instance.username = self.cleaned_data.get('username')
        password_validation.validate_password(self.cleaned_data.get('password2'), self.instance)
        return password2

    def save(self, commit=True):
        user = super(RegisterUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=200,widget=forms.EmailInput(attrs={
        'placeholder':'Email for authentication',
        'class':'form-control'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Your password here.',
        'class':'form-control'
    }))
