from datetime import timedelta
import random
import string
import djclick as click
from faker import Faker
from model_bakery import baker

from fics.models import Author, Character, CustomTag, Fandom, Ship, Fic

from .constants import (
    HARRY_POTTER,
    STAR_WARS,
    SPY_FAMILY,
    GILMORE_GIRLS,
    FANDOMS,
    CHARACTERS,
    SHIPS,
)


fake = Faker()


def create_authors(count: int):
    """
    Generate the number of fake authors in count

    Returns queryset of the Authors that were created.
    """
    ids = []
    for i in range(count):
        obj, created = Author.objects.get_or_create(
            username=fake.user_name(), url=fake.uri()
        )
        if created:
            click.secho(f"---Created author: {obj.username}")
            ids.append(obj.id)

    return Author.objects.filter(id__in=ids)


def create_characters(characters: list):
    """
    Generate the Character objects based on the list of strings in characters

    Returns a queryset of the Characters that were created.
    """
    ids = []
    for character in characters:
        obj, created = Character.objects.get_or_create(name=character)
        if created:
            print(f"---Created character: {character}")
            ids.append(obj.id)

    return Character.objects.filter(id__in=ids)


def create_fandoms(fandoms: list):
    """
    Generate the Fandom objects based on the list of strings in fandoms.

    Returns queryset of the Fandoms that were created.
    """
    ids = []
    for fandom in fandoms:
        obj, created = Fandom.objects.get_or_create(name=fandom)
        if created:
            click.secho(f"---Created fandom: {fandom}")
            ids.append(obj.id)

    return Fandom.objects.filter(id__in=ids)


def create_ships(ships: list):
    """
    Generate the Ship objects based on the list of strings in fandoms.

    Returns queryset of the Ships that were created.
    """
    ids = []
    for ship in ships:
        obj, created = Ship.objects.get_or_create(name=ship)
        if created:
            click.secho(f"---Created ship: {ship}")
            ids.append(obj.id)

    return Ship.objects.filter(id__in=ids)


def create_external_id() -> str:
    """Returns a 10-digit string"""
    result = string.digits
    return "".join(random.choice(result) for i in range(10))


def create_url(external_id: str) -> str:
    """Takes a string. Returns an example URL with that string."""
    return f"https://example.com/fics/{external_id}/"


def create_fic(data: dict) -> Fic:
    """
    Takes a data dictionary. Returns a Fic object.

    Expects this format for `data`:
    {
        "title": str,
        "fandoms": [Fandom],
        "authors": [Author],
        "ships": [Ship],
        "characters": [Character],
    }
    """
    external_id = create_external_id()
    url = create_url(external_id)
    date_published = fake.date_time_this_century()
    date_updated = date_published + timedelta(days=random.randint(1, 30))
    fic, created = Fic.objects.get_or_create(
        title=data.get("title"),
        defaults={
            "url": data.get("url"),
            "external_id": external_id,
            "url": url,
            "complete": random.choice([True, False]),
            "rating": random.choice(Fic.Rating.choices[0]),
            "summary": fake.paragraph(),
            "date_published": date_published,
            "date_updated": date_updated,
        },
    )
    for fandom in data.get("fandoms"):
        fic.fandoms.add(fandom)

    for author in data.get("authors"):
        fic.authors.add(author)

    for ship in data.get("ships"):
        fic.ships.add(ship)

    for character in data.get("characters"):
        fic.characters.add(character)

    return fic

# def get_ships_from_fandom(fandom: str, ships) -> list:
#     """Takes a fandom str, returns the queryset of ships for that fandom"""
#     ships = SHIPS.get(fandom)
#     # breakpoint()
#     if not ships:
#         raise Exception(f"No ships found for {fandom}")
#     return ships.filter(name__in=ships)



@click.command()
def command():
    click.secho("Hello", fg="red")

    # Create tags
    click.secho("Creating tags...", fg="green")
    with open("fics/management/commands/tags.txt", "r") as f:
        lines = f.readlines()
        for tag in lines:
            _, created = CustomTag.objects.get_or_create(name=tag)
            if created:
                click.secho(f"---Created tag: {tag}")

    tags = CustomTag.objects.all()

    # Create authors
    # click.secho("Creating authors...", fg="green")
    # authors = create_authors(30)

    # Create fandoms
    click.secho("Creating fandoms...", fg="green")
    fandoms = create_fandoms(FANDOMS)

    # Create ships
    click.secho("Creating ships...", fg="green")
    ships = create_ships(SHIPS)

    # Create characters
    click.secho("Creating characters...", fg="green")
    characters = create_characters(CHARACTERS)



    click.secho("Creating fics...", fg="green")

    click.secho("Creating Harry Potter fics...", fg="green")
    fandom = fandoms.filter(name__icontains="Harry").first()

    # Get titles
    click.secho("Retrieving titles...", fg="green")
    with open("fics/management/commands/titles.txt", "r") as f:
        lines = f.readlines()
        titles = [title for title in lines if title]

    for i, title in enumerate(titles):
        # Make Harry Potter fics
        if i < 25:
            pass
        # Make Star Wars fics
        elif i < 50:
            pass
        # Make Spy x Family fics
        elif i < 75:
            pass
        # Make Gilmore Girls fics
        else:
            pass
        fic_characters = characters.objects.filter(name__in=HARRY_POTTER_CHARACTERS)
        fic_ships = ships.objects.filter(name__in=HARRY_POTTER_SHIPS)
