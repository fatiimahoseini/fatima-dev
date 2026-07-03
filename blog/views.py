from django.shortcuts import render

def blog(request):
    return render(request, "blog/blog.html")

def blog_preview(request):
    return render(request, 'blog/blog_detail.html')