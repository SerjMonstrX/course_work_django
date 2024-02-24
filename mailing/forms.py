from django import forms
from .models import Mailing

class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['title', 'start_time', 'frequency', 'status', 'clients']  # Поля, которые будут отображаться в форме