from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from .models import Mailing, MailingLog
from .forms import MailingForm



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
        # Получаем текущего пользователя
        user = self.request.user
        # Присваиваем текущего пользователя полю user нового продукта
        form.instance.user = user
        # Сохраняем экземпляр модели перед вызовом super().form_valid()
        return super().form_valid(form)


class MailingUpdateView(LoginANdAuthorRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Получаем объект рассылки
        mailing = self.get_object()
        # Передаем туже установленное значение времени рассылки в форму в качестве начального значения
        kwargs['initial']['start_time'] = mailing.start_time
        return kwargs


class MailingDeleteView(LoginANdAuthorRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')


class MailingLogListView(LoginANdAuthorRequiredMixin, ListView):
    model = MailingLog
    template_name = 'mailing/mailing_log_list.html'
    context_object_name = 'mailing:mailing_logs'
