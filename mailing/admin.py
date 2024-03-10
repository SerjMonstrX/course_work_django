from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms import ModelForm

from .models import Client, Mailing, Message, MailingLog


class MailingInline(admin.TabularInline):
    model = Mailing.clients.through


class MailingAdminForm(ModelForm):
    class Meta:
        model = Mailing
        fields = '__all__'
        widgets = {
            'clients': FilteredSelectMultiple(verbose_name='Клиенты', is_stacked=False)
        }


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    inlines = [MailingInline]
    list_display = ('id', 'full_name', 'client_email', 'comment')
    list_filter = ('full_name',)
    search_fields = ('full_name', 'client_email', 'comment')


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    form = MailingAdminForm
    list_display = ('id', 'user', 'title', 'start_time', 'frequency', 'status')
    list_filter = ('user', 'start_time', 'frequency', 'status')
    search_fields = ('user__email', 'title')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'mailing', 'subject')
    list_filter = ('mailing', 'subject')
    search_fields = ('subject',)


@admin.register(MailingLog)
class MailingLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'mailing', 'client', 'attempt_time', 'status', 'server_response')
    list_filter = ('mailing', 'client', 'status')
    search_fields = ('mailing', 'client', 'status', 'server_response')
