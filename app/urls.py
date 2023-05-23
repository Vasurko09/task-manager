from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('register',views.register,name="register"),
    path('login', views.login, name='login'),
    path('logout',views.logout,name="logout"),
    path('dashboard',views.dashboard,name="dashboard"),
    path('create-task',views.createTask,name="create-task"),
    path('view-task',views.viewTask,name="view-task"),
    path('update-task/<str:pk>/',views.updateTask,name="update-task"),
    path('delete-task/<str:pk>/',views.deleteTask,name="delete-task"),
    path('profile-management',views.profile_management,name="profile-management"),
]