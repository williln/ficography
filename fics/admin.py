from django.contrib import admin

from fics.models import Author, Character, CustomTag, Fandom, Fic, Ship


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


class FicAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "show_fandoms",
        "show_ships",
        "show_authors",
        "word_count",
        "complete",
    )
    list_filter = ("fandoms", "ships", "complete")
    search_fields = ("title", "summary", "fandoms__name", "ships__name")

    def show_fandoms(self, obj):
        if obj.fandoms.exists():
            return ", ".join([fandom.name for fandom in obj.fandoms.all()])
        return ""

    def show_ships(self, obj):
        if obj.ships.exists():
            return ", ".join([ship.name for ship in obj.ships.all()])
        return ""

    def show_authors(self, obj):
        if obj.authors.exists():
            return ", ".join([author.username for author in obj.authors.all()])
        return ""


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


admin.site.register(Fic, FicAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Character, CharacterAdmin)
admin.site.register(Fandom, FandomAdmin)
admin.site.register(Ship, ShipAdmin)
admin.site.register(CustomTag, TagAdmin)
