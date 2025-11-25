from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path

from users.views import LoginUser, RegisterUserView, update_avatar, update_bio

app_name='users'

urlpatterns = [
    path('login/', LoginUser.as_view(), name='login' ),
    path('logout/', LogoutView.as_view(), name='logout' ),
    path('register/', RegisterUserView.as_view(), name='register' ),
    path('update-avatar/', update_avatar, name='update-avatar'),  # Новый путь
    path('update-bio/', update_bio, name='update-bio'),  # Новый путь
]

