from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from blog.models import Post, Author


@admin.register(Author)
class AuthorAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("avatar",)
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("avatar",)}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "avatar",
                    )
                },
            ),
        )
    )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "authors",
        "body",
    ]
    search_fields = ("title",)
    list_filter = ("title",)
