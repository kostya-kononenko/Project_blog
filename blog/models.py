from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField


class Author(AbstractUser):
    avatar = models.ImageField(null=True, blank=True, upload_to="images/profile/")
    bio = models.TextField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    facebook_url = models.CharField(max_length=255, null=True, blank=True)
    twitter_url = models.CharField(max_length=255, null=True, blank=True)
    instagram_url = models.CharField(max_length=255, null=True, blank=True)

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
    body = RichTextField(blank=True, null=True)
    post_date = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, related_name="posts")
    likes = models.ManyToManyField(Author, related_name="blog_post")
    snippet = models.CharField(max_length=255)
    post_image = models.ImageField(null=True, blank=True, upload_to="images/")

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f"{self.title} '|' {self.authors}"

    def get_absolute_url(self):
        return reverse("blog:post-list")


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=255)
    body = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} '|' {self.comment_date}"

    def total_comment(self):
        return self.name.count()
