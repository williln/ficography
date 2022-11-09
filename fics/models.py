from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel


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
    word_count = models.PositiveIntegerField(default=0)
    complete = models.BooleanField(default=False)
    rating = models.CharField(max_length=10, choices=Rating.choices, blank=True)
    summary = models.TextField(null=True)
    date_published = models.DateTimeField(null=True)
    date_updated = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Fic"
        verbose_name_plural = "Fics"
