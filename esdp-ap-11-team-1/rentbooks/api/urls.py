from django.urls import path, include
from api import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path



router = DefaultRouter()
router.register('favorites', views.FavoriteBookViewSet, basename='favorites')

urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns += [
    path('books/<int:pk>/', views.CompositionDetailAPIView.as_view(), name='api_book_detail'),
    path('comments/<int:pk>/', views.comment_update_handler, name='comment_update_handler'),
    path('all-chat/', views.ChatAPIView.as_view(), name='chat'),
    path('add-to-favorites', views.AddToFavorites.as_view(), name='add_to_favorites'),
    path('remove-from-favorites', views.RemoveFromFavorites.as_view(), name='remove_from_favorites'),
    path('check-address/', views.AdressIsValidApi.as_view(), name='check_address'),
    path('books/search/', views.search_book_api_view, name='api_book_search'),
    path('book/<int:pk>/get_book_publish_houses/', views.GetBookPublishHouses.as_view(), name='api_get_book_publish_houses'),
    path('book/<int:pk>/get_book_year/', views.GetBookYearByPublishHouse.as_view(), name='api_get_book_year'),
    path('book/<int:pk>/get_book_isbn/', views.GetBookISBNByYear.as_view(), name='api_get_isbn'),
    path('login', obtain_auth_token),
    path('book/<int:pk>/add-comment', views.AddCommentToCompositon.as_view(), name='comment_add'),
    path('book/<int:pk>/list-comments', views.ListCommentsToCompositon.as_view(), name='list_comments'),
    path('usershelf', views.UserShelfApiView.as_view(), name='user_shelf'),
    path('close_usershelf/<int:pk>', views.CloseUserShelf.as_view(), name='close_user_shelf'),
    path('composition/<int:pk>/add_rating', views.AddRatingToCompositon.as_view(), name='composition_add_rating'),
    
    path('create_order', views.CreateOrder.as_view(), name='create_order'),
    path('order/<int:pk>/cancel', views.CancelOrder.as_view(), name='cancel_order'),
    path('order/<int:pk>/decline', views.DeclineOrder.as_view(), name='decline_order'),
    path('order/<int:pk>/approve', views.ApproveOrder.as_view(), name='approve_order'),
    path('order/<int:pk>/start_rent', views.StartFactRent.as_view(), name='start_fact_rent'),
    path('order/<int:pk>/finish_rent', views.FinishFactRent.as_view(), name='finish_fact_rent'),
    
    path('telegram-confirm', views.TelegramConfirm.as_view(), name='confirm_telegram'),
    path('telegram-code', views.TelegramCode.as_view(), name='code_telegram'),
    path('telegram-get-orders', views.GetAllOrders.as_view(), name='orders_telegram'),
    path('telegram-get-my-orders', views.GetAllMyOrders.as_view(), name='my_orders_telegram'),
    path('telegram-order/<int:pk>/start-rent', views.TelegramStartFactRent.as_view(), name='telegram_start_fact_rent'),
    path('telegram-order/<int:pk>/finish-rent', views.TelegramFinishFactRent.as_view(), name='telegram_finish_fact_rent'),
    path('telegram-chat/<int:pk>', views.GetAllChats.as_view(), name='telegram_chat'),
    
    path('create-chat/', views.ChatCreateAPIView.as_view(), name='chat_create'),
    path('composition/admin/all', views.CompositionAllVisible.as_view(), name='composition_all_visible'),
    path('composition/admin/selected', views.CompositionSelectedVisible.as_view(), name='composition_selected_visible'),
]
