from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('reset-password/', views.resetPassword, name='resetPass'),
    path('forgot-password/', views.forgotPassword, name='forgotPass'),
]