from django.contrib import admin

from fics.models import Author, Character


# Admins


class AuthorAdmin(admin.ModelAdmin):
    list_display = ("username", "url")
    search_fields = ("username",)


class CharacterAdmin(admin.ModelAdmin):
    list_display = ("name", "fandom")
    list_filter = ("fandom",)
    search_fields = ("name",)


admin.site.register(Author, AuthorAdmin)
admin.site.register(Character, CharacterAdmin)
