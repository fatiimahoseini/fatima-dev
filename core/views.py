from django.shortcuts import render
from blog.models import Post


def home(request):
    blog_posts = Post.objects.all()[:6]
    context = {"blog_posts": blog_posts}
    return render(request, "core/home.html", context)


def contact(request):
    return render(request, "core/contact.html")
