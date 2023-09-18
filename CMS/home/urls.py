from django.urls import path
from . import views

urlpatterns = [ 
    path('', views.home, name='home'),
    path('user/<int:pk>/', views.showUserDetail, name='user'),
    path('userUpdate/<int:pk>/', views.updateUser, name='userUpdate'),
    path('like/<int:pk>/', views.likeArticle, name='likeArticle'),
]
