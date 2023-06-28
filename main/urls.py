"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from blog.views import (
    AuthorRegisterView,
    AuthorEditPasswordView,
    password_success,
    AuthorDetailView,
    AuthorListView,
    AuthorEditView,
    follow_user,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path("", include("blog.urls", namespace="blog")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/<int:pk>/", AuthorDetailView.as_view(), name="author-detail"),
    path("accounts/user_list", AuthorListView.as_view(), name="author-list"),
    path("follow_user/<int:pk>/", follow_user, name="author-follow"),
    path("accounts/register/", AuthorRegisterView.as_view(), name="author-register"),
    path("accounts/register/edit/", AuthorEditView.as_view(), name="author-register-edit"),
    path("accounts/password/edit/", AuthorEditPasswordView.as_view(), name="author-password-change"),
    path("accounts/password/password_success/", password_success, name="author-password-success"),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
