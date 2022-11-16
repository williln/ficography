import random
import string
from datetime import timedelta

import djclick as click
from faker import Faker

from fics.models import Author, Character, CustomTag, Fandom, Fic, Ship

from .constants import (
    CHARACTERS,
    FANDOMS,
    GILMORE_GIRLS,
    HARRY_POTTER,
    SHIPS,
    SPY_FAMILY,
    STAR_WARS,
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
            "external_id": external_id,
            "url": url,
            "complete": random.choice([True, False]),
            "rating": random.choice(Fic.Rating.choices[0]),
            "summary": fake.paragraph(),
            "date_published": date_published,
            "date_updated": date_updated,
        },
    )
    click.secho(f"---Created fic: {data['title']}", fg="green")
    for fandom in data.get("fandoms"):
        fic.fandoms.add(fandom)
        click.secho(f"--- --- Added fandom: {fandom}", fg="green")

    for author in data.get("authors"):
        fic.authors.add(author)
        click.secho(f"--- --- Added author: {author}", fg="green")

    for ship in data.get("ships"):
        fic.ships.add(ship)
        click.secho(f"--- --- Added ship: {ship}", fg="green")

    for character in data.get("characters"):
        fic.characters.add(character)
        click.secho(f"--- --- Added character: {character}", fg="green")

    if "tags" in data.keys():
        for tag in data.get("tags"):
            fic.tags.add(tag)
            click.secho(f"--- --- Added tag: {tag}", fg="green")

    return fic


def clear():
    """Only delete the objects that aren't static"""
    Author.objects.all().delete()
    Fic.objects.all().delete()


@click.command()
def command():
    click.secho("Deleting old stuff...", fg="red")
    clear()

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
    click.secho("Creating authors...", fg="green")
    authors = create_authors(50)

    # Create fandoms
    click.secho("Creating fandoms...", fg="green")
    fandoms = create_fandoms(FANDOMS)

    # Create ships
    click.secho("Creating ships...", fg="green")
    ships = create_ships(
        SHIPS[HARRY_POTTER]
        + SHIPS[STAR_WARS]
        + SHIPS[SPY_FAMILY]
        + SHIPS[GILMORE_GIRLS]
    )

    # Create characters
    click.secho("Creating characters...", fg="green")
    characters = create_characters(
        CHARACTERS[HARRY_POTTER]
        + CHARACTERS[STAR_WARS]
        + CHARACTERS[SPY_FAMILY]
        + CHARACTERS[GILMORE_GIRLS]
    )

    # Get titles
    click.secho("Retrieving titles...", fg="green")
    with open("fics/management/commands/titles.txt", "r") as f:
        lines = f.readlines()
        titles = [title for title in lines if title]

    click.secho("Creating fics...", fg="green")

    click.secho("Creating Harry Potter fics...", fg="green")
    fandom = fandoms.filter(name__icontains="Harry").first()
    fandom_characters = characters.filter(name__in=CHARACTERS[HARRY_POTTER])
    fandom_ships = ships.filter(name__in=SHIPS[HARRY_POTTER])

    title_i = 0

    for i in range(25):
        # Get title
        title = titles[title_i]
        title_i += 1

        # Get a random amount of authors, characters, ships, and tags
        author = authors.order_by("?").first()
        fic_characters = fandom_characters[: random.randint(0, len(fandom_characters))]
        fic_ships = fandom_ships[: random.randint(0, len(fandom_ships))]
        fic_tags = tags[: random.randint(0, len(tags))]

        data = {
            "title": title,
            "fandoms": [fandom],
            "authors": [author],
            "characters": fic_characters,
            "tags": fic_tags,
            "ships": fic_ships,
        }
        create_fic(data)

    click.secho("Creating Star Wars fics...", fg="green")
    fandom = fandoms.filter(name__icontains="Star").first()
    fandom_characters = characters.filter(name__in=CHARACTERS[STAR_WARS])
    fandom_ships = ships.filter(name__in=SHIPS[STAR_WARS])

    for i in range(25):
        # Get title
        title = titles[title_i]
        title_i += 1

        # Get a random amount of authors, characters, ships, and tags
        author = authors.order_by("?").first()
        fic_characters = fandom_characters[: random.randint(0, len(fandom_characters))]
        fic_ships = fandom_ships[: random.randint(0, len(fandom_ships))]
        fic_tags = tags[: random.randint(0, len(tags))]

        data = {
            "title": title,
            "fandoms": [fandom],
            "authors": [author],
            "characters": fic_characters,
            "tags": fic_tags,
            "ships": fic_ships,
        }
        create_fic(data)

    click.secho("Creating Spy x Family fics...", fg="green")
    fandom = fandoms.filter(name__icontains="Spy").first()
    fandom_characters = characters.filter(name__in=CHARACTERS[SPY_FAMILY])
    fandom_ships = ships.filter(name__in=SHIPS[SPY_FAMILY])

    for i in range(25):
        # Get title
        title = titles[title_i]
        title_i += 1

        # Get a random amount of authors, characters, ships, and tags
        author = authors.order_by("?").first()
        fic_characters = fandom_characters[: random.randint(0, len(fandom_characters))]
        fic_ships = fandom_ships[: random.randint(0, len(fandom_ships))]
        fic_tags = tags[: random.randint(0, len(tags))]

        data = {
            "title": title,
            "fandoms": [fandom],
            "authors": [author],
            "characters": fic_characters,
            "tags": fic_tags,
            "ships": fic_ships,
        }
        create_fic(data)

    click.secho("Creating Gilmore Girls fics...", fg="green")
    fandom = fandoms.filter(name__icontains="Gilmore").first()
    fandom_characters = characters.filter(name__in=CHARACTERS[GILMORE_GIRLS])
    fandom_ships = ships.filter(name__in=SHIPS[GILMORE_GIRLS])

    for i in range(25):
        # Get title
        title = titles[title_i]
        title_i += 1

        # Get a random amount of authors, characters, ships, and tags
        author = authors.order_by("?").first()
        fic_characters = fandom_characters[: random.randint(0, len(fandom_characters))]
        fic_ships = fandom_ships[: random.randint(0, len(fandom_ships))]
        fic_tags = tags[: random.randint(0, len(tags))]

        data = {
            "title": title,
            "fandoms": [fandom],
            "authors": [author],
            "characters": fic_characters,
            "tags": fic_tags,
            "ships": fic_ships,
        }
        create_fic(data)

    click.secho("All done!!!")
