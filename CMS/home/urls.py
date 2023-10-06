from django.urls import path
from . import views

urlpatterns = [
    path('', views.articleList, name='index'),
    path('category/<str:category_name>/', views.articlesByCategory, name='articlesByCategory'),
    path('register/', views.sign_up, name='register'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('user/<int:pk>/', views.showUserDetail, name='user'),
    path('userUpdate/<int:pk>/', views.updateUser, name='userUpdate'),
    path('new_article/', views.newArticle, name='newArticle'),
    path('articleUpdate/<int:pk>/', views.updateArticle, name='articleUpdate'),
    path('articleDelete/<int:pk>/', views.deleteArticle, name='articleDelete'),
    path('article/<int:pk>/', views.articleDetail, name='article'),
    path('article/own/<int:pk>/', views.ownArticleList, name='own'),
    path('like/<int:pk>/', views.likeArticle, name='likeArticle'),
    path('search/', views.search, name='search'),
    path('rate/<int:post_id>/<int:rating>/', views.rateArticle, name='rateArticle'),
]
