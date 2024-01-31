from django.urls import path 
from userauths import views
from django.contrib.auth import views as auth_views

app_name = 'userauths'

urlpatterns = [
    path('sign-up/', views.register_view, name='sign-up'),
    path('sign-in/', views.login_view, name='sign-in'),
    path('base/', views.base_view, name='base'),  # Corrected the path for BaseView
    path('logout/', views.logout_view, name='logout'),
   
]
