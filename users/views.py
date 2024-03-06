from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetDoneView as BasePasswordResetDoneView, LoginView
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import View, CreateView, ListView, UpdateView
from django.views.generic.edit import FormView
from django.http import Http404
from django.shortcuts import redirect
from django.db.models import Q
from users.forms import UserRegisterForm, UserLoginForm
from users.models import User
from .forms import UserSearchForm


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'

    def form_valid(self, form):
        user = form.save(commit=False)

        # Генерируем токен для верификации
        token = default_token_generator.make_token(user)
        user.verification_token = token
        user.save()

        # Создаем ссылку для верификации почты
        verify_url = self.request.build_absolute_uri(
            reverse_lazy('users:verify_email', kwargs={'pk': user.pk, 'token': token})
        )

        # Отправляем письмо для верификации
        subject = 'Подтверждение регистрации'
        message = (f'Пройдите по ссылке для активации аккаунта {verify_url}')
        send_mail(subject, message, None, [user.email])

        return super().form_valid(form)

class UserUpdateView(UpdateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:user_update')
    template_name = 'users/user_edit.html'

class VerifyEmailView(View):
    def get(self, request, pk, token):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404("Пользователь не найден")

        if user.verification_token == token:
            user.is_active = True
            user.save()
            messages.success(request, 'Ваш аккаунт успешно активирован. Вы можете войти.')
            return redirect('users:login')
        else:
            messages.error(request, 'Неверная ссылка для верификации. Пожалуйста, свяжитесь с администратором.')
            return redirect('users:login')


class CustomLoginView(LoginView):
    template_name = 'users/login.html'  # ваш шаблон для входа
    success_url = '/'  # URL, на который нужно перенаправить пользователя после успешной аутентификации
    form_class = UserLoginForm


class PasswordResetView(FormView):
    form_class = PasswordResetForm
    template_name = 'users/password_reset_form.html'
    success_url = reverse_lazy('users:password_reset_done')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
            # Генерируем новый случайный пароль
            new_password = User.objects.make_random_password()
            # Устанавливаем новый пароль для пользователя
            user.set_password(new_password)
            user.save()

            # Отправляем письмо с новым паролем
            subject = 'Сброс пароля'
            message = (f'Ваш новый пароль {new_password}')
            send_mail(subject, message, None, [user.email], html_message=None)

            messages.success(self.request, 'Новый пароль отправлен на ваш email.')
        except User.DoesNotExist:
            messages.error(self.request, 'Пользователь с указанным email не найден.')

        return super().form_valid(form)


class PasswordResetDoneView(BasePasswordResetDoneView):
    template_name = 'users/password_reset_done.html'


User = get_user_model()


class UserListView(ListView):
    model = User
    template_name = 'users/users_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            # Проверяем, является ли запрос допустимым целым числом (ID пользователя)
            if query.isdigit():
                queryset = queryset.filter(Q(id=query) | Q(email__icontains=query))
            else:
                # Если не является допустимым целым числом, выполняем поиск по электронной почте или имени пользователя
                queryset = queryset.filter(email__icontains=query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = UserSearchForm(self.request.GET)
        return context

def toggle_user_activity(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = not user.is_active
    user.save()
    return redirect('users:users_list')
