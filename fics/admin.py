from django.contrib import admin

from fics.models import Author, Character, CustomTag, Fandom, Ship


class AuthorAdmin(admin.ModelAdmin):
    list_display = ("username", "url")
    search_fields = ("username",)


class CharacterAdmin(admin.ModelAdmin):
    list_display = ("name", "fandom")
    list_filter = ("fandom",)
    search_fields = ("name",)


class FandomAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


class ShipAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


admin.site.register(Author, AuthorAdmin)
admin.site.register(Character, CharacterAdmin)
admin.site.register(Fandom, FandomAdmin)
admin.site.register(Ship, ShipAdmin)
admin.site.register(CustomTag, TagAdmin)
