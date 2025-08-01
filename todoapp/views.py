from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .models import todo
from django.contrib.auth.decorators import login_required

# Landing Page
def landing_page(request):
    if request.user.is_authenticated:
        return redirect('home-page')
    return render(request, 'todoapp/base.html')


@login_required
def home(request):
    if request.method == 'POST':
        task = request.POST.get('task')
        if task:
            if todo.objects.filter(user=request.user, todo_name=task).exists():
                messages.error(request, "Task already exists.")
            else:
                new_todo = todo(user=request.user, todo_name=task)
                new_todo.save()

    all_todos = todo.objects.filter(user=request.user)
    return render(request, 'todoapp/todo.html', {'todos': all_todos})

# Register View
def register(request):
    if request.user.is_authenticated:
        return redirect('home-page')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not username or not email or not password or not confirm_password:
            messages.error(request, "All fields are required.")
            return redirect('register')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('register')

        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Choose another.')
            return redirect('register')

        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, 'User successfully created. You can login now.')
        return redirect('login')

    return render(request, 'todoapp/register.html')

# Login View
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home-page')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)
            return redirect('home-page')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'todoapp/login.html')

# Logout View
def LogoutView(request):
    logout(request)
    return redirect('login')

# Delete Task by ID
@login_required
def DeleteTask(request, id):
    task = todo.objects.filter(user=request.user, id=id).first()
    if task:
        task.delete()
    return redirect('home-page')

# Update Task Status by ID
@login_required
def Update(request, id):
    task = todo.objects.filter(user=request.user, id=id).first()
    if task:
        task.status = True
        task.save()
    return redirect('home-page')


@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        user = request.user

        if not user.check_password(current_password):
            messages.error(request, 'Current password is incorrect.')
            return redirect('change-password')

        if new_password != confirm_password:
            messages.error(request, 'New passwords do not match.')
            return redirect('change-password')

        if len(new_password) < 6:
            messages.error(request, 'Password must be at least 6 characters long.')
            return redirect('change-password')

        user.set_password(new_password)
        user.save()

        update_session_auth_hash(request, user)

        messages.success(request, 'Password updated successfully.')
        return redirect('login')

    return render(request, 'todoapp/change_password.html')
