from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext as _


from blog.models import Post, Author, Category, Comment


@admin.register(Author)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
        (
            _(
                "Additional info",
            ),
            {
                "fields": (
                    "bio",
                    "date_of_birth",
                    "avatar",
                    "facebook_url",
                    "twitter_url",
                    "instagram_url",
                    "follows",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "bio",
                    "date_of_birth",
                    "avatar",
                    "facebook_url",
                    "twitter_url",
                    "instagram_url",
                    "follows",
                ),
            },
        ),
    )
    list_display = ("email", "first_name", "last_name", "is_staff")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "authors",
        "body",
    ]
    search_fields = ("title",)
    list_filter = ("title",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "comment_date",
    ]
    search_fields = ("name",)
    list_filter = ("name",)


admin.site.register(Category)
