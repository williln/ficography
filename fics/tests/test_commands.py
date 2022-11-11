from model_bakery import baker
from test_plus.test import TestCase

from fics.management.commands.constants import (
    HARRY_POTTER_SHIPS,
    HARRY_POTTER,
    STAR_WARS,
    SPY_FAMILY,
    GILMORE_GIRLS,
    FANDOMS,
    CHARACTERS,
    SHIPS,
)
from fics.management.commands.load_sample_fics import (
    create_authors,
    create_characters,
    create_external_id,
    create_fandoms,
    create_fic,
    create_ships,
    create_url,
    get_ships_from_fandom,
)
from fics import models


class LoadSampleFicsTestCase(TestCase):
    def test_create_authors(self):
        count = models.Author.objects.count()
        result = create_authors(1)
        self.assertEquals(models.Author.objects.count(), count + 1)

    def test_create_characters(self):
        count = models.Character.objects.count()
        result = create_characters(["Harry", "Hermione"])
        self.assertEquals(models.Character.objects.count(), count + 2)
        self.assertTrue(models.Character.objects.filter(name="Harry").exists())
        self.assertTrue(models.Character.objects.filter(name="Hermione").exists())

    def test_create_fandoms(self):
        count = models.Fandom.objects.count()
        result = create_fandoms(["Sample"])
        self.assertEquals(models.Fandom.objects.count(), count + 1)
        self.assertTrue(models.Fandom.objects.filter(name="Sample").exists())

    def test_create_fic(self):
        # FIXME
        pass

    def test_create_ships(self):
        count = models.Ship.objects.count()
        result = create_ships(["Sample", "Another sample"])
        self.assertEquals(models.Ship.objects.count(), count + 2)
        self.assertTrue(models.Ship.objects.filter(name="Sample").exists())

    def test_create_external_id(self):
        result = create_external_id()
        self.assertEqual(type(result), str)

    def test_create_url(self):
        result = create_url("hermione")
        self.assertEquals(result, "https://example.com/fics/hermione/")

    def test_get_ships_from_fandom(self):
        expected = HARRY_POTTER_SHIPS
        # result = get_ships_from_fandom(HARRY_POTTER)
        # FIXME
        # self.assertEquals(set(expected), set(result))

