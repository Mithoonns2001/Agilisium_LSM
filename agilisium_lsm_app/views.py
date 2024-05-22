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

from django.views import View
from dotenv import load_dotenv
import google.generativeai as genai
import os

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
            batch=request.POST['batch'],
            email=request.POST['email'],
            password=hashed_pw,
            role=request.POST['role'],
            # secret_password=request.POST['secret_password']

        )
        # Create a session
        # request.session['user_id'] = new_user.id
        # if new_user.role=='employee':
        #     redirect_url = f'/user/{new_user.id}/my_dashboard'
        #     return redirect(redirect_url)
        # if new_user.role=='head':
        #     redirect_url = f'/head/events_list'
        #     return redirect(redirect_url)
        redirect_url = f'/{new_user.id}/dashboard'

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
    return render(request, 'user_dashboard.html', {'user_id': user_id})

def admin_dashboard(request, user_id):
    user = User.objects.get(pk=user_id)

    return render(request, 'admin_dashboard.html', {'user_id': user_id, 'user':user})

def logout(request):
    request.session.flush()
    return redirect('/')

def learning_labs(request, user_id):
        # return redirect('events_list')
    return render(request, 'learning_labs.html', {'user_id': user_id})

def tasks(request, user_id):
    tasks = Task.objects.all()
    user = User.objects.get(pk=user_id)
    return render(request, 'tasks.html', { 'tasks':tasks, 'user_id': user_id, 'user': user})

def create_task(request, user_id):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        image = request.FILES.get('image')  # Get the uploaded image file

        # Create event and event dates
        task = Task.objects.create(name=name, description=description, image=image)

        return redirect(f'/{user_id}/tasks')

    return render(request, 'create_task.html', {'user_id': user_id})

def open_task(request, user_id, task_id):
    users = User.objects.all()

    task = get_object_or_404(Task, pk=task_id)
    return render(request, 'open_task.html', {'task':task, 'user_id': user_id, 'users':users})


def learnings(request, user_id):
    all_materials = Material.objects.all()
    user = User.objects.get(pk=user_id)
    return render(request, 'learnings.html', { 'user_id': user_id, 'user': user, 'all_materials':all_materials})

def upload_material(request, user_id):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        material = request.FILES.get('material')  # Get the uploaded image file

        # Create event and event dates
        upload_material = Material.objects.create(name=name, description=description, material=material)

        return redirect(f'/{user_id}/learnings')

    return render(request, 'upload_material.html', {'user_id': user_id})


def graduation_labs(request, user_id):
    return render(request, 'graduation_labs.html', {'user_id': user_id})


def deliverables(request, user_id):
    deliverables = Deliverables.objects.all()
    user = User.objects.get(pk=user_id)
    return render(request, 'deliverables.html', { 'deliverables':deliverables, 'user_id': user_id, 'user': user})

def create_deliverables(request, user_id):
    if request.method == 'POST':
        name = request.POST['name']

        deliverables = Deliverables.objects.create(name=name)

        return redirect(f'/{user_id}/deliverables')

    return render(request, 'create_deliverables.html', {'user_id': user_id})

def open_deliverables(request, user_id, task_id):
    users = User.objects.all()

    deliverable = get_object_or_404(Deliverables, pk=task_id)
    return render(request, 'open_deliverable.html', {'deliverable':deliverable, 'user_id': user_id, 'users':users})


######
# Load environment variables
load_dotenv()

# Configure generative AI
genai.configure(api_key=os.getenv("GENAI_API_KEY"))

# Function to load Gemini Pro model and get response
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

class ChatView(View):
    template_name = 'chat.html'

    def get(self, request):
        chat_history = request.session.get('chat_history', [])
        return render(request, self.template_name, {'chat_history': chat_history})

    def post(self, request):
        user_input = request.POST.get('input')
        if user_input:
            response = get_gemini_response(user_input)
            chat_history = request.session.get('chat_history', [])
            chat_history.append(("You", user_input))
            for chunk in response:
                chat_history.append(("Bot", chunk.text))
            request.session['chat_history'] = chat_history
        return redirect('/chat')