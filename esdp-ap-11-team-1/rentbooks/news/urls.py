from django.urls import path

from news.views import NewsListView, NewsCreateView, NewsDetailView, NewsUpdateView, NewsDeleteView

urlpatterns = [
    path('', NewsListView.as_view(), name='news_list'),
    path('add', NewsCreateView.as_view(), name='news_create'),
    path('<int:pk>', NewsDetailView.as_view(), name='news_detail'),
    path('<int:pk>/update', NewsUpdateView.as_view(), name='news_update'),
    path('<int:pk>/delete', NewsDeleteView.as_view(), name='news_delete'),
    path('<int:pk>/confirm_delete', NewsDeleteView.as_view(), name='news_confirm_delete'),
]
