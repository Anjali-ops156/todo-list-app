from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('dashboard/', views.home, name='home-page'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.LogoutView, name='logout'),
    path('delete-task/<int:id>/', views.DeleteTask, name='delete'),
    path('update/<int:id>/', views.Update, name='update'),

    # ✅ Password Reset URL (without email, with custom template)
    path(
        "change-password/",
        PasswordChangeView.as_view(
            template_name="todoapp/change_password.html",
            success_url=reverse_lazy('login')
        ),
        name="change-password"
    ),
]
