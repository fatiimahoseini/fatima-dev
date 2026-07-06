from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Post, Category, Tag


def blog(request):
    posts = Post.objects.all()

    # Category filter
    category_slug = request.GET.get("category")
    if category_slug:
        posts = posts.filter(category__slug=category_slug)

    # Tag filter
    tag_slug = request.GET.get("tag")
    if tag_slug:
        posts = posts.filter(tags__slug=tag_slug)

    # Search
    query = request.GET.get("q")
    if query:
        posts = posts.filter(
            Q(title__icontains=query)
            | Q(excerpt__icontains=query)
            | Q(content__icontains=query)
        )

    # Reading time filter
    reading_time = request.GET.get("reading_time")
    if reading_time:
        if reading_time == "under-5":
            posts = posts.filter(read_time__lt=5)
        elif reading_time == "5-10":
            posts = posts.filter(read_time__gte=5, read_time__lte=10)
        elif reading_time == "10-plus":
            posts = posts.filter(read_time__gt=10)

    # Sorting
    sort = request.GET.get("sort", "latest")
    if sort == "oldest":
        posts = posts.order_by("published_at")
    elif sort == "popular":
        posts = posts.order_by("-views_count")
    else:
        posts = posts.order_by("-published_at")

    featured_posts = Post.objects.filter(is_featured=True)[:3]
    categories = Category.objects.all()
    tags = Tag.objects.all()

    context = {
        "posts": posts,
        "featured_posts": featured_posts,
        "categories": categories,
        "tags": tags,
        "current_sort": sort,
        "current_category": category_slug,
        "current_tag": tag_slug,
        "current_query": query or "",
        "current_reading_time": reading_time,
    }
    return render(request, "blog/blog.html", context)


def blog_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)

    # Increment views
    Post.objects.filter(pk=post.pk).update(views_count=post.views_count + 1)

    previous_post = post.get_previous_post()
    next_post = post.get_next_post()

    context = {
        "post": post,
        "previous_post": previous_post,
        "next_post": next_post,
    }
    return render(request, "blog/blog_detail.html", context)
