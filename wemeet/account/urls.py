from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.Register.as_view(), name='register'),
    path('profile/', views.Profile.as_view(), name='profile'),
    path('reset-password/', views.ChangeUserPassowrd.as_view(), 
    	name='reset_password'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activateAccount, name='activate'),
]