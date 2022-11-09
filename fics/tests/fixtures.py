import pytest
from model_bakery import baker


@pytest.fixture
def fic(db):
    return baker.make("fics.Fic")
