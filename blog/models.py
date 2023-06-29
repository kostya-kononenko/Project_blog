from django.utils.translation import gettext as _
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class Author(AbstractUser):
    avatar = models.ImageField(null=True, blank=True, upload_to="images/profile/")
    bio = models.TextField(null=True, blank=True)
    username = None
    email = models.EmailField(_("email address"), unique=True)

    date_of_birth = models.DateField(null=True, blank=True)
    facebook_url = models.CharField(max_length=255, null=True, blank=True)
    twitter_url = models.CharField(max_length=255, null=True, blank=True)
    instagram_url = models.CharField(max_length=255, null=True, blank=True)
    follows = models.ManyToManyField(
        "self", related_name="followed_by", symmetrical=False, blank=True
    )
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def count_followers(self):
        return self.follows.count()

    def count_following(self):
        return Author.objects.filter(follows=self).count()

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
