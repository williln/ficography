from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from taggit.managers import TaggableManager
from taggit.models import GenericTaggedItemBase, TagBase


class Author(TimeStampedModel):
    username = models.CharField(max_length=255)
    url = models.URLField()

    def __str__(self):
        return self.username


class Character(TimeStampedModel):
    """
    The canon characters in the fic. Generally original characters will come through
    with something generic like "Original Character"
    """

    name = models.CharField(max_length=255)
    fandom = models.ForeignKey(
        "fics.Fandom", related_name="characters", on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return self.name


class Fandom(TimeStampedModel):
    """
    A 'fandom' is the community around a specific thing.
    With respect to fics, 'Hary Potter' and 'Star Wars' are both fandoms.
    """

    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = _("Fandom")
        verbose_name_plural = _("Fandoms")

    def __str__(self):
        return self.name


class Ship(TimeStampedModel):
    """
    A 'ship' is a relationship. -
    'Harry Potter/Ginny Weasley' is a ship. -
    """

    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = _("Ship")
        verbose_name_plural = _("Ships")

    def __str__(self):
        return self.name


# Custom tags


class CustomTag(TagBase):
    explicit = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")


class TaggedFic(GenericTaggedItemBase):
    tag = models.ForeignKey(
        "fics.CustomTag",
        on_delete=models.CASCADE,
        related_name="tags",
    )


class Fic(TimeStampedModel):
    class Rating(models.TextChoices):
        EXPLICIT = "EXPLICIT", _("Explicit")
        GENERAL = "GENERAL", _("General")
        MATURE = "MATURE", _("Mature")
        NR = "NR", _("Not Rated")
        TEEN = "TEEN", _("Teen and Up")

    title = models.CharField(max_length=255)
    url = models.URLField()
    external_id = models.CharField(
        null=True,
        max_length=100,
        help_text="ID of the work on the platform (AO3, FFN, etc.)",
    )
    fandoms = models.ManyToManyField("fics.Fandom", related_name="fics")
    authors = models.ManyToManyField("fics.Author", related_name="fics")
    ships = models.ManyToManyField("fics.Ship", related_name="fics")
    characters = models.ManyToManyField("fics.Character", related_name="fics")
    word_count = models.PositiveIntegerField(default=0)
    complete = models.BooleanField(default=False)
    rating = models.CharField(max_length=10, choices=Rating.choices, blank=True)
    summary = models.TextField(null=True)
    date_published = models.DateTimeField(null=True)
    date_updated = models.DateTimeField(null=True)

    tags = TaggableManager(through=TaggedFic)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Fic"
        verbose_name_plural = "Fics"
