from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('register', views.register),
    path('login', views.login),
    path('user/<int:user_id>/my_dashboard/', views.my_dashboard_user, name='my_dashboard_user'),  
    path('head/admin_dashboard', views.admin_dashboard, name='admin_dashboard'),

    path('logout', views.logout, name='logout'),

] 