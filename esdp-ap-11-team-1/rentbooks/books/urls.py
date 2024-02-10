from django.urls import path, include
from rest_framework import routers

from books import views 
from .views.book import BookImageViewSet


router = routers.SimpleRouter()
router.register(r'book', BookImageViewSet)

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    
    path('add_genre', views.AddGenreView.as_view()),
    path('new_test', views.AddBookView.as_view()),    # создание composition
    path('new_test1', views.BookView.as_view()),      # создание book
    
    path('book_create/', views.BookCreateView.as_view(), name='create_book'),
    path('book/<int:pk>/update/', views.BookUpdateView.as_view(), name='update_book'),
    path('book/<int:pk>/confirm_delete/', views.BookDeleteView.as_view(), name='confirm_delete'),
    path('books/', views.SearchCompositionView.as_view(), name='books_list'),
    path('book_image/', include(router.urls)),          # http://127.0.0.1:8000/book_image/book/
    
    path('composition_create/', views.CompositionCreateView.as_view(), name='create_composition'),
    path('composition/<int:pk>/details/', views.CompositionDetailView.as_view(), name='detail_composition'),
    path('composition/<int:pk>/update/', views.CompositionUpdateView.as_view(), name='update_composition'),
    path('composition/<int:pk>/composition_delete/', views.CompositionDeleteView.as_view(), name='composition_delete'),
    path('list_compositions/', views.ListOfCompositionsView.as_view(), name='list_compositions'),
    
    path('comment_add/<int:pk>/', views.add_comment, name='comment_add'),
    path('book/<int:pk>/to_favor/', views.favorite_unfavor, name='favor_unfavor'),
    path('book/<int:pk>/delete_favorite/', views.delete_from_favorite, name='delete_favorite'),
    path('composition/admin/', views.CompositionAdminListView.as_view(), name='composition_admin'),
    path('create_book', views.AllInOneView.as_view(),name='create_all_book'),      # создание book
]
