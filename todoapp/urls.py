from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('delete-task/<int:id>/', views.delete_task, name='delete-task'),
    path('update/<int:id>/', views.mark_as_done, name='update-task'),
    path('change-password/', views.manual_change_password, name='change-password'),
]
