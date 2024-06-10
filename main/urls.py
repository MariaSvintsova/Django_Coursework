from django.urls import path, include


from main.views import NewsLetterDetailView, NewsLetterCreateView, NewsLetterUpdateView, NewsLetterDeleteView, \
    NewsLetterListView
from main.apps import MainConfig
from django.contrib import admin

app_name = MainConfig.name

urlpatterns = [
    path('create/', NewsLetterCreateView.as_view(), name='newsletter_form'),
    path('<int:pk>/', NewsLetterDetailView.as_view(), name='newsletter_detail'),
    path('update/<int:pk>', NewsLetterUpdateView.as_view(), name='newsletter_update'),
    path('delete/<int:pk>', NewsLetterDeleteView.as_view(), name='newsletter_delete'),
    path('', NewsLetterListView.as_view(), name='newsletter_list'),
]