from django import forms

from users.forms import CustomFormMixin
from .models import Mailing, Message



class MailingForm(CustomFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['message'].queryset = Message.objects.filter(user=user)

    class Meta:
        model = Mailing
        fields = ['title', 'start_time', 'start_date', 'end_date', 'frequency', 'status', 'clients', 'message']
        widgets = {
            'start_time': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }


class MessageForm(CustomFormMixin, forms.ModelForm):

    class Meta:
        model = Message
        fields = ['subject', 'body']