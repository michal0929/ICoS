from django import forms
from users.models import *
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

class AddUser(forms.ModelForm):
    class Meta:
        model = UserProfile
        widgets = {
            'password': forms.PasswordInput(),
        }
        fields = ['username', 'password', 'email', 'is_professor', 'is_site_admin']


class EditUser(forms.ModelForm):
    class Meta:
        model = UserProfile
        widgets = {
            'password': forms.PasswordInput(),
        }
        fields = ['username', 'password', 'email', 'is_professor', 'is_site_admin']

    # Don't want to modify blank setting inside models (doing so will break normal validation in admin site)
    # The redefined constructor won't harm any functionality.
    def __init__(self, *args, **kwargs):
        super(EditUser, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = False

class UpdateUser(forms.ModelForm):
    class Meta:
        model = UserProfile
        widgets = {
            'password': forms.PasswordInput(),
        }
        fields = ['username','password', 'email']

    # Don't want to modify blank setting inside models (doing so will break normal validation in admin site)
    # The redefined constructor won't harm any functionality.
    def __init__(self, *args, **kwargs):
        super(UpdateUser, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = False

class Contact(forms.Form):
    sender = forms.CharField(label='Name', max_length=30)
    subject = forms.CharField(label='Subject', max_length=30)
    email = forms.EmailField(label='Email', max_length=30)
    message = forms.CharField(widget=forms.Textarea)

class UserDetailsChangeForm(forms.Form):
    first_name = forms.CharField(max_length=150,
                                 required=False,
                                 label=mark_safe('<i class="uk-icon-user "></i> Name'),
                                 widget=forms.TextInput(attrs={'placeholder': 'Name', 'class': "uk-width-1-1"}))

    last_name = forms.CharField(max_length=150,
                                required=False,
                                label=mark_safe('<i class="uk-icon-user "></i> Surname'),
                                widget=forms.TextInput(attrs={'placeholder': 'Surname', 'class': "uk-width-1-1"}))


    username = forms.RegexField(regex=r'^[\w.@+-]+$',
                                max_length=150,
                                label=mark_safe('<i class="uk-icon-user-secret"></i> Username'),
                                help_text="Username can contain only letters, numbers and @/./+/-/_ characters.",
                                error_messages={'invalid': "This value may contain only letters, numbers and @/./+/-/_ characters."},
                                widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': "uk-width-1-1"}))

    email = forms.EmailField(max_length=150,
                             label=mark_safe('<i class="uk-icon-envelope"></i> e-mail'),
                             widget=forms.TextInput(attrs={'placeholder': 'Email', 'class': "uk-width-1-1"}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(UserDetailsChangeForm, self).__init__(*args, **kwargs)


    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exclude(id=self.user.id).exists():
            raise ValidationError("A user with that username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exclude(id=self.user.id).exists():
            raise ValidationError("Email is already in use.")
        return email

    def clean(self):
        if 'submit' in self.data:
            form_data = self.cleaned_data
            return form_data

class UserPasswordChangeForm(forms.Form):
    old_password = forms.CharField(max_length=150,
                                   label=mark_safe('<i class="uk-icon-lock"></i> Old password'),
                                   widget=forms.PasswordInput(attrs={'placeholder': 'Old password', 'class': "uk-width-1-1"}))

    new_password = forms.CharField(max_length=150,
                                   label=mark_safe('<i class="uk-icon-unlock"></i> New password '),
                                   widget=forms.PasswordInput(attrs={'placeholder': 'New password', 'class': "uk-width-1-1"}))

    repeat_new_password = forms.CharField(max_length=150,
                                      label=mark_safe('<i class="uk-icon-unlock"></i> Repeat new password'),
                                      widget=forms.PasswordInput(attrs={'placeholder': 'Repeat new password', 'class': "uk-width-1-1"}))
 
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(UserPasswordChangeForm, self).__init__(*args, **kwargs)


    def clean_old_password(self):
        valid = self.user.check_password(self.cleaned_data['old_password'])
        if not valid:
             raise forms.ValidationError("Password incorrect")
        return valid

    def clean(self):
        if 'submitPass' in self.data:
            form_data = self.cleaned_data
            if form_data['new_password'] != form_data['repeat_new_password']:
                self.add_error('repeat_new_password', "Password does not match")
                # raise ValidationError("Passwords does not match")
            return form_data