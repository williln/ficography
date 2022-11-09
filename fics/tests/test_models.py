from faker import Faker
from model_bakery import baker
from test_plus.test import TestCase

from ..models import Author, Fic

fake = Faker()


class AuthorModelTests(TestCase):
    def setUp(self):
        self.author = baker.make("fics.Author")

    def test_object_creation(self):
        Author.objects.create(username=fake.user_name(), url=fake.uri())

    def test_str(self):
        self.assertEquals(str(self.author), self.author.username)


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
