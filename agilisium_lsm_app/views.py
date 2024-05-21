from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib import messages
from django.utils.dateparse import parse_date
from django.core.exceptions import ValidationError
from datetime import datetime
from django.http import HttpResponseForbidden
from .models import *
import bcrypt
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings  # Import Django settings module

def register(request):
    if request.method == 'POST':
        errors = User.objects.Validate_Registration(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        # Create a user
        new_user = User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            emp_id=request.POST['emp_id'],
            email=request.POST['email'],
            password=hashed_pw,
            role=request.POST['role'],
            # secret_password=request.POST['secret_password']

        )
        # Create a session
        request.session['user_id'] = new_user.id
        if new_user.role=='employee':
            redirect_url = f'/user/{new_user.id}/my_dashboard'
            return redirect(redirect_url)
        if new_user.role=='head':
            redirect_url = f'/head/events_list'
            return redirect(redirect_url)
    return redirect('/')


def login(request):
    if request.method == 'POST':
        log_email = request.POST['log_email']
        log_password = request.POST['log_password']
        log_role = request.POST['log_role']
        print(log_role)
        try:
            user = User.objects.get(email=log_email, role=log_role)
        except User.DoesNotExist:
            messages.error(request, 'Invalid email or password 2')
            return redirect('/')

        if bcrypt.checkpw(log_password.encode(), user.password.encode()):
        # Store user_id in session
            request.session['user_id'] = user.id

            # Construct the redirect URL based on the user's role
            # if log_role == 'employee':
            #     redirect_url = f'/{user.id}/my_dashboard'
            # elif log_role == 'head':
            redirect_url = f'/{user.id}/dashboard'

            return redirect(redirect_url)


    return redirect('/')


def index(request):
    return render(request, 'index.html')


def my_dashboard_user(request, user_id):
    # Assuming user_id is obtained from the session
    # If not, you need to handle the logic to retrieve user_id
    # from session or any other source
    return render(request, 'user_dashboard.html', {'user_id': user_id})

def admin_dashboard(request, user_id):
    # Assuming user_id is obtained from the session
    # If not, you need to handle the logic to retrieve user_id
    # from session or any other source
    return render(request, 'admin_dashboard.html', {'user_id': user_id})

def logout(request):
    request.session.flush()
    return redirect('/')

def learning_labs(request, user_id):
        # return redirect('events_list')
    return render(request, 'learning_labs.html', {'user_id': user_id})

def tasks(request, user_id):
    tasks = Task.objects.all()

    return render(request, 'tasks.html', { 'tasks':tasks, 'user_id': user_id})

def create_task(request, user_id):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        image = request.FILES.get('image')  # Get the uploaded image file

        # Create event and event dates
        task = Task.objects.create(name=name, description=description, image=image)

        return redirect(f'/{user_id}/tasks')

    return render(request, 'create_task.html', {'user_id': user_id})

def open_task(request, user_id):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        image = request.FILES.get('image')  # Get the uploaded image file

        # Create event and event dates
        task = Task.objects.create(name=name, description=description, image=image)


    return render(request, 'open_task.html', {'task':task, 'user_id': user_id})

def open_task(request, user_id, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, 'open_task.html', {'task':task, 'user_id': user_id})


