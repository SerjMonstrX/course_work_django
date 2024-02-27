from django.urls import path
from .views import (HomeView, MailingListView, MailingCreateView, MailingUpdateView, MailingDeleteView,
                    MailingLogListView)

app_name = 'mailing'


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('mailings/', MailingListView.as_view(), name='mailing_list'),
    path('mailings/create/', MailingCreateView.as_view(), name='create_mailing'),
    path('mailings/<int:pk>/update/', MailingUpdateView.as_view(), name='update_mailing'),
    path('mailings/<int:pk>/delete/', MailingDeleteView.as_view(), name='delete_mailing'),
    path('mailings/logs/', MailingLogListView.as_view(), name='mailing_log_list'),
]
print()