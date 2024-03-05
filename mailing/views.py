from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView, DetailView
from django.urls import reverse_lazy, reverse
from .models import Mailing, MailingLog, Message
from .forms import MailingForm, MessageForm


class LoginANdAuthorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Класс, объединяющий общие настройки для проверки авторства пользователя"""

    def test_func(self):
        """Функция для проверки является ли пользователь автором рассылки"""
        mailing = self.get_object()
        return self.request.user == mailing.user


class HomeView(TemplateView):
    template_name = 'mailing/home.html'


class MailingListView(ListView):
    model = Mailing
    template_name = 'mailing/mailing_list.html'
    context_object_name = 'mailing:mailings'


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        return super().form_valid(form)

    def get_form_kwargs(self):
        # Получаем ключевые аргументы для формы
        kwargs = super().get_form_kwargs()
        # Изменяем аргументы формы, добавляя пользователя в их начальные значения
        kwargs['initial'] = {'user': self.request.user, 'status': 'created', 'frequency': 'daily'}
        kwargs['user'] = self.request.user
        return kwargs


class MailingUpdateView(LoginANdAuthorRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        return super().form_valid(form)



class MailingDeleteView(LoginANdAuthorRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')


class MailingDetailView(LoginANdAuthorRequiredMixin, DetailView):
    model = Mailing



class MailingLogListView(LoginANdAuthorRequiredMixin, ListView):
    model = MailingLog
    template_name = 'mailing/mailing_log_list.html'
    context_object_name = 'mailing:mailing_logs'


class MessageListView(ListView):
    model = Message
    template_name = 'mailing/message_list.html'
    context_object_name = 'mailing:message_list'


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:message_list')

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        return super().form_valid(form)

    def get_form_kwargs(self):
        # Получаем ключевые аргументы для формы
        kwargs = super().get_form_kwargs()
        # Изменяем аргументы формы, добавляя пользователя в их начальные значения
        kwargs['initial'] = {'user': self.request.user}
        return kwargs


class MessageUpdateView(LoginANdAuthorRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        return super().form_valid(form)

class MessageDeleteView(LoginANdAuthorRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:message_list')
