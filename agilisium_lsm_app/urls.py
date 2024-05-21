from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('register', views.register),
    path('login', views.login),
    path('user/<int:user_id>/my_dashboard/', views.my_dashboard_user, name='my_dashboard_user'),  
    path('<int:user_id>/dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('<int:user_id>/learning_labs', views.learning_labs, name='learning_labs'),
    path('<int:user_id>/tasks', views.tasks, name='tasks'),
    path('<int:user_id>/create_task/', views.create_task, name='create_task'),

    path('logout', views.logout, name='logout'),

] 