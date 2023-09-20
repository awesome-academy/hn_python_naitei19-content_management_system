from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.sign_up, name='register'),
    path('user/<int:pk>/', views.showUserDetail, name='user'),
    path('userUpdate/<int:pk>/', views.updateUser, name='userUpdate'),
]
