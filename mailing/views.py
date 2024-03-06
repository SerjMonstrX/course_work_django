from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import render
from blog.models import BlogPost
from .models import Mailing, MailingLog, Message, Client
from .forms import MailingForm, MessageForm, ModeratorMailingForm, ModeratorMessageForm, ClientForm, ModeratorClientForm


class LoginANdAuthorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Класс, объединяющий общие настройки для проверки авторства пользователя"""

    def test_func(self):
        """Функция для проверки является ли пользователь автором рассылки"""
        mailing = self.get_object()
        return self.request.user == mailing.user


class HomeView(TemplateView):
    template_name = 'mailing/home.html'

    def get(self, request):
        """Функция вывода статистики на главной странице"""
        total_mailings = Mailing.objects.count()    # Количество рассылок всего
        active_mailings = Mailing.objects.filter(status='started').count()  # Количество активных рассылок
        unique_clients = Client.objects.count()    # Количество уникальных клиентов для рассылок
        articles = BlogPost.objects.order_by('?')[:3]    # 3 случайные статьи из блога

        context = {
            'total_mailings': total_mailings,
            'active_mailings': active_mailings,
            'unique_clients': unique_clients,
            'articles': articles,
        }
        return render(request, 'mailing/home.html', context)


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
    success_url = reverse_lazy('mailing:mailing_list')

    def get_form_class(self):
        """Вывод формы для модератора/юзера в зависимости от того, кто в сессии"""
        if self.request.user.is_staff and not self.request.user == self.get_object().user:
            return ModeratorMailingForm
        else:
            return MailingForm

    def get_form_kwargs(self):
        mailing = self.get_object()
        # Получаем ключевые аргументы для формы
        kwargs = super().get_form_kwargs()
        kwargs['user'] = mailing.user
        return kwargs

    def test_func(self):
        """Функция для проверки является ли пользователь автором рассылки (используется UserPassesTestMixin)"""
        mailing = self.get_object()
        return self.request.user == mailing.user or self.request.user.is_staff  # Модератор или автор поста


class MailingDeleteView(LoginANdAuthorRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')


class MailingDetailView(LoginANdAuthorRequiredMixin, DetailView):
    model = Mailing

    def test_func(self):
        """Функция для проверки является ли пользователь автором рассылки (используется UserPassesTestMixin)"""
        mailing = self.get_object()
        return self.request.user == mailing.user or self.request.user.is_staff  # Модератор или автор поста


class MailingLogListView(ListView):
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
    success_url = reverse_lazy('mailing:message_list')

    def get_form_class(self):
        if self.request.user.is_staff and not self.request.user == self.get_object().user:
            return ModeratorMessageForm
        else:
            return MessageForm

    def test_func(self):
        """Функция для проверки является ли пользователь автором сообщения"""
        message = self.get_object()
        return self.request.user == message.user or self.request.user.is_staff  # Модератор или автор поста


class MessageDetailView(LoginANdAuthorRequiredMixin, DetailView):
    model = Message

    def test_func(self):
        """Функция для проверки является ли пользователь автором рассылки (используется UserPassesTestMixin)"""
        mailing = self.get_object()
        return self.request.user == mailing.user or self.request.user.is_staff  # Модератор или автор поста


class MessageDeleteView(LoginANdAuthorRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:message_list')


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailing/client_form.html'
    success_url = reverse_lazy('mailing:client_list')

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


class ClientUpdateView(LoginANdAuthorRequiredMixin, UpdateView):
    model = Client
    success_url = reverse_lazy('mailing:client_list')

    def get_form_class(self):
        if self.request.user.is_staff and not self.request.user == self.get_object().user:
            return ModeratorClientForm
        else:
            return ClientForm

    def test_func(self):
        """Функция для проверки является ли пользователь автором сообщения"""
        message = self.get_object()
        return self.request.user == message.user or self.request.user.is_staff  # Модератор или автор поста


class ClientDetailView(LoginANdAuthorRequiredMixin, DetailView):
    model = Client

    def test_func(self):
        """Функция для проверки является ли пользователь автором рассылки (используется UserPassesTestMixin)"""
        client = self.get_object()
        return self.request.user == client.user or self.request.user.is_staff  # Модератор или автор поста


class ClientListView(ListView):
    model = Client
    template_name = 'mailing/client_list.html'
    context_object_name = 'mailing:client_list'


class ClientDeleteView(LoginANdAuthorRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:client_list')
