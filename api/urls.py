from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken import views


from api.views import PostViewSet, CommentViewSet, CategoryViewSet, CreateAuthorView, AuthorViewSet, CreateTokenView

router = routers.DefaultRouter()
router.register("posts", PostViewSet)
router.register("authors", AuthorViewSet)
router.register("category`s", CategoryViewSet)
router.register("comments", CommentViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("create/author/", CreateAuthorView.as_view(), name="api-create-author"),
    path('token/', CreateTokenView.as_view(), name="token")
]
app_name = "api"
