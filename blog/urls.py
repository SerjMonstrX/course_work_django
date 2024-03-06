from django.urls import path

from blog.apps import BlogConfig
from blog.views import (
    BlogCreateView,
    BlogListView,
    BlogDetailView,
    BlogUpdateView,
    BlogDeleteView,
)

app_name = BlogConfig.name

urlpatterns = [
    path('create/', BlogCreateView.as_view(), name='create'),
    path('<slug:slug>/', BlogDetailView.as_view(), name='detail'),
    path('<slug:slug>/edit/', BlogUpdateView.as_view(), name='edit'),
    path('<slug:slug>/delete/', BlogDeleteView.as_view(), name='delete'),
    path('', BlogListView.as_view(), name='list'),
]
