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
    list_display = ("name", "show_characters", "show_fandoms")
    list_filter = ("characters__fandom",)
    search_fields = ("name",)

    def show_characters(self, obj):
        if obj.characters.exists():
            return ", ".join([character.name for character in obj.characters.all()])
        return ""

    def show_fandoms(self, obj):
        if obj.characters.exists():
            fandoms = [
                character.fandom
                for character in obj.characters.all().distinct("fandom")
            ]
            return ", ".join([fandom.name for fandom in fandoms])
        return ""


class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


admin.site.register(Author, AuthorAdmin)
admin.site.register(Character, CharacterAdmin)
admin.site.register(Fandom, FandomAdmin)
admin.site.register(Ship, ShipAdmin)
admin.site.register(CustomTag, TagAdmin)
