from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
from django import forms


class CustomFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserRegisterForm(CustomFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserLoginForm(CustomFormMixin, AuthenticationForm):
    class Meta:
        model = User
        fields = ('email', 'password')


class UserEditForm(CustomFormMixin, forms.Form):

    q = forms.CharField(label='Search', required=False)
    model = User
    fields = ('email', 'password1', 'password2')


class PasswordResetRequestForm(CustomFormMixin, forms.Form):
    email = forms.EmailField(label='Email')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError('Пожалуйста, введите ваш адрес электронной почты.')
        return email


class UserSearchForm(forms.Form):
    q = forms.CharField(label='Search', required=False)
