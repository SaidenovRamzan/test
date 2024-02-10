from django.urls import path
from accounts import views


urlpatterns = [
    path('accounts/register/', views.UserRegistrationView.as_view(), name='registration'),
    path('accounts/profile/', views.UserProfileView.as_view(), name='user_profile'),
    path('accounts/profile/update/<int:pk>', views.UserProfileUpdateView.as_view(), name='update_profile'),
    path('accounts/user_ratio/<int:pk>/<int:rt>', views.user_ratio, name='user_ratio'),
    path('accounts/user_page/<int:pk>', views.UserPageView.as_view(), name='user_page'),
]