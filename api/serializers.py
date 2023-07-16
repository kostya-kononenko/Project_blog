from rest_framework import serializers
from django.contrib.auth import get_user_model

from blog.models import Post, Author, Comment, Category


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "first_name",
            "last_name",
            "password",
            "avatar",
            "bio",
            "email",
            "date_of_birth",
            "facebook_url",
            "twitter_url",
            "instagram_url",
            "follows",
        )
        read_only_fields = ("id", "is_staff")
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)


class AuthorDetailSerializer(AuthorSerializer):
    follows = serializers.SlugRelatedField(many=True, read_only=True, slug_field="first_name")


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("name", "body", "comment_date")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"


class PostDetailSerializer(PostSerializer):
    category = CategorySerializer(many=True, read_only=True)
    authors = AuthorDetailSerializer(many=False, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    likes = serializers.SlugRelatedField(many=True, read_only=True, slug_field="first_name")


class PostListSerializer(PostSerializer):
    category = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")
    authors = serializers.StringRelatedField(many=False)
    comments = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")
