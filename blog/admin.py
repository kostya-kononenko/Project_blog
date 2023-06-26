from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from blog.models import Post, Author, Category


@admin.register(Author)
class AuthorAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("bio",
                                             "date_of_birth")

    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": (
            "bio",
            "date_of_birth",
            "avatar",
            "facebook_url",
            "twitter_url",
            "instagram_url",
            )}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "bio",
                        "date_of_birth",
                        "avatar",
                        "facebook_url",
                        "twitter_url",
                        "instagram_url",
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


admin.site.register(Category)
