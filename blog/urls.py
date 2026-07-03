from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog, name='blog'),
    # path('<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('preview/', views.blog_preview, name='blog_detail'),
]