from django import forms

from users.forms import CustomFormMixin
from .models import Mailing, Message, Client


class MailingForm(CustomFormMixin, forms.ModelForm):
    clients = forms.ModelMultipleChoiceField(queryset=Client.objects.none(), widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['message'].queryset = Message.objects.filter(user=user)
        self.fields['clients'].queryset = Client.objects.filter(user=user)

    class Meta:
        model = Mailing
        fields = ['title', 'start_time', 'start_date', 'end_date', 'frequency', 'status', 'message', 'clients']
        widgets = {
            'start_time': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }


class MessageForm(CustomFormMixin, forms.ModelForm):

    class Meta:
        model = Message
        fields = ['subject', 'body']

class ModeratorMailingForm(CustomFormMixin, forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['title', 'start_time', 'start_date', 'end_date', 'frequency', 'status', 'message', 'clients']
        widgets = {
            'start_time': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Запрещаем редактирование полей, кроме 'status'
        for field_name, field in self.fields.items():
            if field_name != 'status':
                field.disabled = True

class ModeratorMessageForm(CustomFormMixin, forms.ModelForm):

    class Meta:
        model = Message
        fields = ['subject', 'body']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Запрещаем редактирование полей, кроме 'status'
        for field_name, field in self.fields.items():
            field.disabled = True


class ClientForm(CustomFormMixin, forms.ModelForm):

    class Meta:
        model = Client
        fields = ['client_email', 'full_name', 'comment']

class ModeratorClientForm(CustomFormMixin, forms.ModelForm):

    class Meta:
        model = Client
        fields = ['client_email', 'full_name', 'comment']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Запрещаем редактирование полей
        for field_name, field in self.fields.items():
            field.disabled = True