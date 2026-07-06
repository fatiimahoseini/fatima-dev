from django.db import models
from django.utils.text import slugify


ICON_CHOICES = [
    ("list", "List / All"),
    ("django", "Django"),
    ("python", "Python"),
    ("code", "Code / Web Dev"),
    ("briefcase", "Career / Work"),
    ("lightbulb", "Ideas / Thoughts"),
    ("database", "Database"),
    ("api", "API"),
    ("server", "Server / Backend"),
    ("globe", "Internet / Frontend"),
    ("lock", "Security"),
    ("terminal", "Terminal"),
    ("rocket", "Deployment"),
    ("star", "Featured"),
    ("heart", "Favorites"),
]

ICON_COLORS = {
    "list": "text-white",
    "django": "text-green-400",
    "python": "text-yellow-400",
    "code": "text-slate-300",
    "briefcase": "text-slate-300",
    "lightbulb": "text-purple-400",
    "database": "text-blue-400",
    "api": "text-cyan-400",
    "server": "text-orange-400",
    "globe": "text-blue-400",
    "lock": "text-red-400",
    "terminal": "text-green-400",
    "rocket": "text-sky-400",
    "star": "text-amber-400",
    "heart": "text-pink-400",
}

ICON_SVG = {
    "list": '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 6h16M4 12h16M4 18h16"/>',
    "django": '<path d="M6 3v18h4.5c4.5 0 7.5-3 7.5-9s-3-9-7.5-9H6z"/>',
    "python": '<path d="M12 2c-4 0-4 3-4 3v3h8V5s0-3-4-3z"/><path d="M12 22c4 0 4-3 4-3v-3H8v3s0 3 4 3z"/>',
    "code": '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M16 18l6-6-6-6M8 6l-6 6 6 6"/>',
    "briefcase": '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 7h18v12H3V7z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 7V5h6v2"/>',
    "lightbulb": '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 3a3 3 0 013 3v12a3 3 0 01-6 0V6a3 3 0 013-3z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 3a3 3 0 013 3v12a3 3 0 01-6 0V6a3 3 0 013-3z"/>',
    "database": '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 7c0-1.657 3.582-3 8-3s8 1.343 8 3M4 7v10c0 1.657 3.582 3 8 3s8-1.343 8-3V7M4 7c0 1.657 3.582 3 8 3s8-1.343 8-3M4 12c0 1.657 3.582 3 8 3s8-1.343 8-3"/>',
    "api": '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>',
    "server": '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M5 12h14M5 12a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v4a2 2 0 01-2 2M5 12a2 2 0 00-2 2v4a2 2 0 002 2h14a2 2 0 002-2v-4a2 2 0 00-2-2m-2-4h.01M17 16h.01"/>',
    "globe": '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9"/>',
    "lock": '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>',
    "terminal": '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>',
    "rocket": '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15.59 14.37a6 6 0 01-5.84 7.38v-4.8m5.84-2.58a14.98 14.98 0 006.16-12.12A14.98 14.98 0 009.631 8.41m5.96 5.96a14.926 14.926 0 01-5.841 2.58m-.119-8.54a6 6 0 00-7.381 5.84h4.8m2.581-5.84a14.927 14.927 0 00-2.58 5.84m2.699 2.7c-.103.021-.207.041-.311.06a15.09 15.09 0 01-2.448-2.448 14.9 14.9 0 01.06-.312m-2.24 2.39a4.493 4.493 0 00-1.757 4.306 4.493 4.493 0 004.306-1.758M16.5 9a1.5 1.5 0 11-3 0 1.5 1.5 0 013 0z"/>',
    "star": '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"/>',
    "heart": '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>',
}


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    icon = models.CharField(max_length=50, choices=ICON_CHOICES, default="list")

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_icon_svg(self):
        return ICON_SVG.get(self.icon, ICON_SVG["list"])


class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to="blog/")
    excerpt = models.TextField(max_length=500)
    content = models.TextField()
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="posts"
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name="posts")
    read_time = models.PositiveIntegerField(help_text="Reading time in minutes")
    is_featured = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)
    published_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_previous_post(self):
        return Post.objects.filter(published_at__lt=self.published_at).first()

    def get_next_post(self):
        return Post.objects.filter(published_at__gt=self.published_at).last()
