from django.urls import path
from . import views

urlpatterns = [
    path("", views.blog, name="blog"),
    path("subscribe/", views.newsletter_subscribe, name="newsletter_subscribe"),
    path("<slug:slug>/", views.blog_detail, name="blog_detail"),
]
