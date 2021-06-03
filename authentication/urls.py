from django.contrib.auth import logout
from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import login, register

urlpatterns = [
    path('', login, name='login'),
    path('register/', register),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]
