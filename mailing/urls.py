from django.urls import path
from .views import (HomeView, MailingListView, MailingCreateView, MailingUpdateView, MailingDeleteView,
                    MailingLogListView, MessageCreateView, MessageDeleteView, MessageListView,
                    MailingDetailView, MessageUpdateView, MessageDetailView, ClientDetailView, ClientUpdateView,
                    ClientDeleteView, ClientListView, ClientCreateView)

app_name = 'mailing'


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('mailings/', MailingListView.as_view(), name='mailing_list'),
    path('mailings/create/', MailingCreateView.as_view(), name='create_mailing'),
    path('mailings/<int:pk>/detail/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailings/<int:pk>/update/', MailingUpdateView.as_view(), name='update_mailing'),
    path('mailings/<int:pk>/delete/', MailingDeleteView.as_view(), name='delete_mailing'),
    path('mailings/logs/', MailingLogListView.as_view(), name='mailing_log_list'),
    path('mailings/message/create/', MessageCreateView.as_view(), name='create_message'),
    path('mailings/message/<int:pk>/detail/', MessageDetailView.as_view(), name='message_detail'),
    path('mailings/message/<int:pk>/update/', MessageUpdateView.as_view(), name='update_message'),
    path('mailings/message/<int:pk>/delete/', MessageDeleteView.as_view(), name='delete_message'),
    path('mailings/messages', MessageListView.as_view(), name='message_list'),
    path('mailings/client/create/', ClientCreateView.as_view(), name='create_client'),
    path('mailings/client/<int:pk>/detail/', ClientDetailView.as_view(), name='client_detail'),
    path('mailings/client/<int:pk>/update/', ClientUpdateView.as_view(), name='update_client'),
    path('mailings/client/<int:pk>/delete/', ClientDeleteView.as_view(), name='delete_client'),
    path('mailings/clients', ClientListView.as_view(), name='client_list'),
]
