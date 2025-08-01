from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from .models import todo  # Your Task model



def landing_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'todoapp/base.html')


@login_required
def home(request):
    if request.method == 'POST':
        task_name = request.POST.get('task')

        if task_name:
            
            if todo.objects.filter(user=request.user, todo_name=task_name).exists():
                messages.error(request, "Task already exists.")
            else:
                todo.objects.create(user=request.user, todo_name=task_name)

    
    todos = todo.objects.filter(user=request.user)
    return render(request, 'todoapp/todo.html', {'todos': todos})


# Register View
def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

      
        if not username or not email or not password or not confirm_password:
            messages.error(request, "All fields are required.")
        elif password != confirm_password:
            messages.error(request, "Passwords do not match.")
        elif len(password) < 6:
            messages.error(request, "Password must be at least 6 characters.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        else:
          
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect('login')

    return render(request, 'todoapp/register.html')


# Login View
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if 'next' in request.GET:
        messages.info(request, "Please login to access that page.")

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            auth_login(request, user)
            next_url = request.GET.get('next')
            return redirect(next_url if next_url else 'home')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'todoapp/login.html')
# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')


# Delete Task by ID
@login_required
def delete_task(request, id):
    task = get_object_or_404(todo, id=id, user=request.user)
    task.delete()
    return redirect('home')


@login_required
def mark_as_done(request, id):
    task = get_object_or_404(todo, id=id, user=request.user)
    task.status = True
    task.save()
    return redirect('home')


def manual_change_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not username or not new_password or not confirm_password:
            messages.error(request, "All fields are required.")
        elif new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
        elif len(new_password) < 6:
            messages.error(request, "Password must be at least 6 characters.")
        else:
            try:
                user = User.objects.get(username=username)
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password changed successfully. You can now log in.")
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, "User not found.")

    return render(request, 'todoapp/change_password.html')