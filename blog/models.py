from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Author(AbstractUser):
    avatar = models.ImageField()

    class Meta:
        verbose_name = "author"
        verbose_name_plural = "authors"


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255)
    title_tag = models.CharField(max_length=255)
    authors = models.ForeignKey(Author, on_delete=models.CASCADE)
    body = models.TextField()
    post_date = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, related_name="posts")
    likes = models.ManyToManyField(Author, related_name="blog_post")

    def __str__(self):
        return f"{self.title} '|' {self.authors}"

    def get_absolute_url(self):
        return reverse("blog:post-list")
