from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import ChatView

urlpatterns = [
    path('', views.index, name='home'),
    path('register', views.register),
    path('login', views.login),
    path('user/<int:user_id>/my_dashboard/', views.my_dashboard_user, name='my_dashboard_user'),  
    path('<int:user_id>/dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('<int:user_id>/learning_labs', views.learning_labs, name='learning_labs'),
    path('<int:user_id>/tasks', views.tasks, name='tasks'),
    path('<int:user_id>/open_task/<int:task_id>', views.open_task, name='open_task'),

    path('<int:user_id>/create_task/', views.create_task, name='create_task'),


    path('<int:user_id>/learnings', views.learnings, name='learnings'),
    path('<int:user_id>/upload_material/', views.upload_material, name='upload_material'),


    path('<int:user_id>/graduation_labs', views.graduation_labs, name='graduation_labs'),

    path('<int:user_id>/deliverables', views.deliverables, name='deliverables'),
    path('<int:user_id>/create_deliverables/', views.create_deliverables, name='create_deliverables'),
    path('<int:user_id>/open_deliverables/<int:task_id>', views.open_deliverables, name='open_deliverables'),

    path('chat', ChatView.as_view(), name='ChatView'),  

    path('logout', views.logout, name='logout'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)