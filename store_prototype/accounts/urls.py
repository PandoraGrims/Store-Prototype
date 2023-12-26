from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from accounts.views import RegisterView, ProfileView, UserPasswordChangeView, UserChangeView


app_name = "accounts"

urlpatterns = [
    path('login/', LoginView.as_view(template_name="login.html"), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('register/', RegisterView.as_view(), name="register"),
    path('<int:pk>/profile/', ProfileView.as_view(), name="profile"),
    path('<int:pk>/change/', UserChangeView.as_view(), name='change'),
    path('password-change/', UserPasswordChangeView.as_view(), name='password_change'),
]
