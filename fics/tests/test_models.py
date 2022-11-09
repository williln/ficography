import pytest

from model_bakery import baker
from test_plus.test import TestCase

from ..models import Fic


@pytest.mark.django_db()
class FicModelTests(TestCase):
    def setUp(self):
        self.fic = baker.make("fics.Fic")

    def test_fic_creation(self):
        Fic.objects.create(
            url="www.example.com",
            title="Example",
        )

    def test_fic_str(self):
        assert str(self.fic) == f"{self.fic.title}"
