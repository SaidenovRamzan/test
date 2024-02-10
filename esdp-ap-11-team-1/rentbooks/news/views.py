from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from news.forms import NewsForm
from news.models import News


# Create your views here.

class NewsListView(ListView):
    template_name = 'news_list.html'

    context_object_name = 'news'
    model = News
    ordering = ['-updated_at']

    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset().exclude(is_deleted=True)
        return queryset


class NewsDetailView(DetailView):
    template_name = 'news_detail.html'
    model = News


class NewsCreateView(LoginRequiredMixin, CreateView):
    template_name = 'news_create.html'
    model = News
    form_class = NewsForm

    def get_success_url(self):
        return reverse('news_detail', kwargs={'pk': self.object.pk})


class NewsUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'news_update.html'
    model = News
    form_class = NewsForm

    def get_success_url(self):
        return reverse('news_detail', kwargs={'pk': self.object.pk})


class NewsDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'news_delete.html'
    model = News

    def get_success_url(self):
        return reverse('news_list')
