from django.urls import path, include

from blog.views import HomeView, PostDetailView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("post/<int:pk>", PostDetailView.as_view(), name="post-detail"),
]

app_name = "blog"
