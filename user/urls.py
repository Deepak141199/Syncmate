from django.urls import path
from .views import CreateUserView, CustomAuthToken, UserProfileView

urlpatterns = [
    path('register/', CreateUserView.as_view(), name='register'),
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
]
