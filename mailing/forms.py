from django import forms
from .models import Mailing, Client


class MailingForm(forms.ModelForm):
    clients = forms.ModelMultipleChoiceField(
        queryset=Client.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-select-multiple-scroll'})
    )

    class Meta:
        model = Mailing
        fields = ['title', 'start_time', 'frequency', 'status', 'clients']
        widgets = {
            'start_time': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
        }