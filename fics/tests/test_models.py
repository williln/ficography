from faker import Faker
from model_bakery import baker
from test_plus.test import TestCase

from ..models import Author, CustomTag, Fandom, Fic

fake = Faker()


class AuthorModelTests(TestCase):
    def setUp(self):
        self.author = baker.make("fics.Author")

    def test_object_creation(self):
        Author.objects.create(username=fake.user_name(), url=fake.uri())

    def test_str(self):
        self.assertEquals(str(self.author), self.author.username)


class FandomModelTests(TestCase):
    def setUp(self):
        self.fandom = baker.make("fics.Fandom")

    def test_object_creation(self):
        Fandom.objects.create(name="Spy x Family")

    def test_str(self):
        self.assertEquals(str(self.fandom), self.fandom.name)


class FicModelTests(TestCase):
    def setUp(self):
        self.fic = baker.make("fics.Fic")

    def test_fic_creation(self):
        Fic.objects.create(
            url="www.example.com",
            title="Example",
        )

    def test_fic_str(self):
        self.assertEquals(str(self.fic), self.fic.title)


class TagModelTests(TestCase):
    def setUp(self):
        self.tag = baker.make("fics.CustomTag")
        self.explicit_tag = baker.make("fics.CustomTag", explicit=True)
        self.fic = baker.make("fics.fic")

    def test_object_creation(self):
        self.tag = CustomTag.objects.create(name="tagged")

    def test_tagging_fic(self):
        self.fic.tags.add(self.tag)
        self.fic.tags.add(self.explicit_tag)
        self.assertIn(self.tag, self.fic.tags.all())
        self.assertIn(self.explicit_tag, self.fic.tags.all())
        self.assertTrue(self.explicit_tag.explicit)
        self.assertTrue(self.fic.tags.filter(explicit=True).exists())
