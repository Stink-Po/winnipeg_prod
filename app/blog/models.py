from django.db import models
from django.utils import timezone
from accounts.models import CustomUser
from django.urls import reverse
from taggit.managers import TaggableManager
from django.utils.text import slugify


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset() \
            .filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    title = models.CharField(max_length=250)
    subtitle = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date="publish")
    author = models.ForeignKey(CustomUser,
                               on_delete=models.CASCADE,
                               related_name="blog_posts")
    body = models.TextField()
    tags = TaggableManager()
    image = models.ImageField(upload_to="post_images", null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)

    objects = models.Manager()  # The Default Manager
    published = PublishedManager()  # Our Custom Manager

    class Meta:
        ordering = ["-publish"]
        indexes = models.Index(fields=["-publish"]),

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[
            self.publish.year,
            self.publish.month,
            self.publish.day,
            self.slug,
        ])

    def save(self, *args, **kwargs):
        # Generate slug from title if not provided
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)
