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
        username = fake.user_name()
        url = create_url(username)
        obj, created = Author.objects.get_or_create(username=username, url=url)
        if created:
            click.secho(f"---Created author: {obj.username}")
        ids.append(obj.id)

    return Author.objects.filter(id__in=ids)


def create_characters(characters: list, fandom: Fandom):
    """
    Generate the Character objects based on the list of strings in characters,
    and adds the fandom

    Returns a queryset of the Characters that were created.
    """
    ids = []
    for character in characters:
        obj, created = Character.objects.update_or_create(name=character, fandom=fandom)
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
    Generate the Ship objects based on the list of strings in fandoms,
    and connects the characters for the ship to the Ship object

    Returns queryset of the Ships that were created.
    """
    ids = []
    for ship in ships:
        obj, created = Ship.objects.get_or_create(name=ship)
        if created:
            click.secho(f"---Created ship: {ship}")
        ids.append(obj.id)

        # Add characters
        characters = ship.split("/")
        try:
            character_a = Character.objects.get(name__icontains=characters[0])
            character_b = Character.objects.get(name__icontains=characters[1])
            obj.characters.add(character_a)
            obj.characters.add(character_b)
        except Character.DoesNotExist:
            continue

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
    Character.objects.all().delete()
    Fandom.objects.all().delete()
    Ship.objects.all().delete()
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
    create_fandoms(FANDOMS)

    hp_fandom = Fandom.objects.get(name__icontains="Harry")
    sw_fandom = Fandom.objects.get(name__icontains="Star")
    spy_fandom = Fandom.objects.get(name__icontains="Spy")
    gg_fandom = Fandom.objects.get(name__icontains="Gilmore")

    # Create characters
    click.secho("Creating Harry Potter characters...", fg="green")
    hp_characters = create_characters(CHARACTERS[HARRY_POTTER], hp_fandom)

    click.secho("Creating Star Wars characters...", fg="green")
    sw_characters = create_characters(CHARACTERS[STAR_WARS], sw_fandom)

    click.secho("Creating Spy x Family characters...", fg="green")
    sf_characters = create_characters(CHARACTERS[SPY_FAMILY], spy_fandom)

    click.secho("Creating Gilmore Girls characters...", fg="green")
    gg_characters = create_characters(CHARACTERS[GILMORE_GIRLS], gg_fandom)

    # Create ships
    click.secho("Creating ships...", fg="green")
    ships = create_ships(
        SHIPS[HARRY_POTTER]
        + SHIPS[STAR_WARS]
        + SHIPS[SPY_FAMILY]
        + SHIPS[GILMORE_GIRLS]
    )

    # Get titles
    click.secho("Retrieving titles...", fg="green")
    with open("fics/management/commands/titles.txt", "r") as f:
        lines = f.readlines()
        titles = [title for title in lines if title]

    click.secho("Creating fics...", fg="green")

    click.secho("Creating Harry Potter fics...", fg="green")
    fandom = hp_fandom
    fandom_characters = hp_characters
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
    fandom = sw_fandom
    fandom_characters = sw_characters
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
    fandom = spy_fandom
    fandom_characters = sf_characters
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
    fandom = gg_fandom
    fandom_characters = gg_characters
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
