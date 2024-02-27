from django import forms
from .models import Mailing, Client



class MailingForm(forms.ModelForm):
    clients = forms.ModelMultipleChoiceField(
        queryset=Client.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-select-multiple-scroll'}),
        required=False
    )
    new_clients = forms.CharField(max_length=100, label='Новые клиенты', required=False,
                                   help_text='Введите адреса электронной почты новых клиентов, разделяя их запятыми')

    class Meta:
        model = Mailing
        fields = ['title', 'start_time', 'frequency', 'status', 'clients']
        widgets = {
            'start_time': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
        }

    def clean_new_clients(self):
        """Метод для обработки новых клиентов"""
        data = self.cleaned_data['new_clients']
        if data:
            # Разбиваем строку на адреса электронной почты, разделенные запятыми
            email_list = [email.strip() for email in data.split(',') if email.strip()]
            return email_list
        return []

    def save(self, commit=True):
        mailing = super().save(commit=False)
        if commit:
            mailing.save()

            # Добавляем новых клиентов
            new_clients = self.cleaned_data.get('new_clients')
            if new_clients:
                for email in new_clients:
                    client, created = Client.objects.get_or_create(client_email=email)
                    mailing.clients.add(client)
        return mailing