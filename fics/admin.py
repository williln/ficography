from django.contrib import admin

from fics.models import Author


class AuthorAdmin(admin.ModelAdmin):
    list_display = ("username", "url")
    search_fields = ("username",)


admin.site.register(Author, AuthorAdmin)
