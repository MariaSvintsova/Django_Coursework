from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from rest_framework import generics
from main.forms import NewsLetterForm
from main.models import NewsLetter


class NewsLetterListView(ListView):
    """ NewsLetter list edpoint """
    model = NewsLetter
    form_class = NewsLetterForm
    template_name = 'newsletter_list.html'

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            queryset = NewsLetter.objects.all()
        else:
            queryset = NewsLetter.objects.filter(user=user)

        return queryset


class NewsLetterDetailView(DetailView):
    """ NewsLetter detail edpoint """

    model = NewsLetter
    template_name = 'newsletter_detail.html'
    success_url = reverse_lazy('main:newsletter_list')


class NewsLetterCreateView(CreateView):
    """ NewsLetter create edpoint """

    model = NewsLetter
    form_class = NewsLetterForm
    template_name = 'main/newsletter_form.html'
    success_url = reverse_lazy('main:newsletter_list')

    def form_valid(self, form):
        # Устанавливаем текущего пользователя как автора рассылки
        form.instance.user = self.request.user
        # Вызываем родительский метод для сохранения данных формы
        return super().form_valid(form)


class NewsLetterUpdateView(UpdateView):
    """ NewsLetter update edpoint """

    model = NewsLetter
    form_class = NewsLetterForm
    template_name = 'newsletter_form.html'
    success_url = reverse_lazy('main:newsletter_list')


class NewsLetterDeleteView(DeleteView):
    """ NewsLetter delete edpoint """

    model = NewsLetter
    template_name = 'newsletter_delete.html'
    success_url = reverse_lazy('main:newsletter_list')


