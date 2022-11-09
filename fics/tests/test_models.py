from ..models import Fic


def test_work_creation(db):
    Fic.objects.create(
        url="www.example.com",
        title="Example",
    )


def test_work_str(fic):
    assert str(fic) == f"{fic.title}"
