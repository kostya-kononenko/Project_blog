from django.urls import path, include

from blog.views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    CategoryListView,
    CategoryDetailView,
    CategoryCreateView,
    CategoryUpdateView,
    CategoryDeleteView,
    LikeView,
    CommentCreateView,
)


urlpatterns = [
    path("", PostListView.as_view(), name="post-list"),
    path("post/<int:pk>", PostDetailView.as_view(), name="post-detail"),
    path("post/create/", PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
    path("post/<int:pk>/comment/", CommentCreateView.as_view(), name="comment-create"),
    path("category/", CategoryListView.as_view(), name="category-list"),
    path("category/<int:pk>", CategoryDetailView.as_view(), name="category-detail"),
    path("category/create/", CategoryCreateView.as_view(), name="category-create"),
    path(
        "category/<int:pk>/update/",
        CategoryUpdateView.as_view(),
        name="category-update",
    ),
    path(
        "category/<int:pk>/delete/",
        CategoryDeleteView.as_view(),
        name="category-delete",
    ),
    path("like/<int:pk>", LikeView, name="like_post"),
]

app_name = "blog"
