from django.contrib.auth.models import AbstractUser
from django.db import models


class Author(AbstractUser):
    avatar = models.ImageField()

    class Meta:
        verbose_name = "author"
        verbose_name_plural = "authors"


class Post(models.Model):
    title = models.CharField(max_length=255)
    title_tag = models.CharField(max_length=255, default="tag")
    authors = models.ForeignKey(Author, on_delete=models.CASCADE)
    body = models.TextField()

    def __str__(self):
        return f"{self.title} '|' {self.authors}"

