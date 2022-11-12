from model_bakery import baker
from test_plus.test import TestCase

from fics import models
from fics.management.commands.constants import (
    CHARACTERS,
    FANDOMS,
    GILMORE_GIRLS,
    HARRY_POTTER,
    HARRY_POTTER_SHIPS,
    SHIPS,
    SPY_FAMILY,
    STAR_WARS,
)
from fics.management.commands.load_sample_fics import (  # get_ships_from_fandom,
    create_authors,
    create_characters,
    create_external_id,
    create_fandoms,
    create_fic,
    create_ships,
    create_url,
)


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
        fandom = baker.make("fics.Fandom")
        author = baker.make("fics.Author")
        ship = baker.make("fics.Ship")
        character_1 = baker.make("fics.Character")
        character_2 = baker.make("fics.Character")
        data = {
            "title": "Sample",
            "url": "https://example.com/fics/sample/",
            "fandoms": [fandom],
            "authors": [author],
            "ships": [ship],
            "characters": [character_1, character_2],
        }
        result = create_fic(data)
        self.assertTrue(result)
        self.assertIsNotNone(result.pk)
        self.assertEquals(result.title, data["title"])
        self.assertIn(fandom, result.fandoms.all())
        self.assertIn(author, result.authors.all())
        self.assertIn(character_1, result.characters.all())
        self.assertIn(character_2, result.characters.all())

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

    # def test_get_ships_from_fandom(self):
    #     # Set up ships
    #     for ship in SHIPS:
    #         models.Ship.objects.get_or_create(name=ship)
    #     expected = models.Ship.objects.filter(name__in=HARRY_POTTER_SHIPS)
    #     result = get_ships_from_fandom(HARRY_POTTER, models.Ship.objects.all())
    #     self.assertEquals(expected, result)
