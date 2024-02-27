from django.urls import path
from users.views import RegisterView, CustomLoginView, VerifyEmailView, PasswordResetView, PasswordResetDoneView, \
    UserListView, toggle_user_activity
from django.contrib.auth.views import LogoutView

app_name = 'users'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('verify_email/<int:pk>/<str:token>/', VerifyEmailView.as_view(), name='verify_email'),
    path('reset_password/', PasswordResetView.as_view(), name='password_reset'),
    path('reset_password/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('users_list/', UserListView.as_view(), name='users_list'),
    path('toggle-user-activity/<int:user_id>/', toggle_user_activity, name='toggle_user_activity'),
]