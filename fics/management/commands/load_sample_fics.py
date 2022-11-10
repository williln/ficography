import djclick as click
from faker import Faker
from model_bakery import baker

from fics.models import Author, Character, CustomTag, Fandom, Ship


fake = Faker()

FANDOMS = [
    "Harry Potter - J. K. Rowling",
    "Star Wars - All Media Types",
    "SPY x FAMILY (Anime)",
    "Gilmore Girls"
]

HARRY_POTTER_CHARACTERS = [
    "Harry Potter",
    "Hermione Granger",
    "Draco Malfoy",
    "Ron Weasley",
    "Sirius Black",
    "Remus Lupin",
    "Severus Snape",
    "James Potter",
    "Ginny Weasley",
    "Albus Dumbledore"
]

HARRY_POTTER_SHIPS = [
    "Draco Malfoy/Harry Potter",
    "Sirius Black/Remus Lupin",
    "Hermione Granger/Draco Malfoy",
    "Hermione Granger/Ron Weasley",
    "Harry Potter/Ginny Weasley"
]

STAR_WARS_CHARACTERS = [
    "Rey (Star Wars)",
    "Obi-Wan Kenobi",
    "Ben Solo | Kylo Ren",
    "Leia Organa",
    "Armitage Hux",
    "Poe Dameron",
    "Anakin Skywalker",
    "Luke Skywalker",
    "Padme Amidala"
]

STAR_WARS_SHIPS = [
    "Rey/Ben Solo | Kylo Ren",
    "Padme Amidala/Anakin Skywalker",
]

SPY_CHARACTERS = [
    "Loid Forger | Twilight",
    "Anya Forger",
    "Yor Briar Forger | Thorn Princess"
]

SPY_SHIPS = ["Loid Forger | Twilight/Yor Briar Forger | Thorn Princess"]

GILMORE_CHARACTERS = [
    "Rory Gilmore",
    "Lorelai Gilmore",
    "Luke Danes",
    "Jess Mariano",
    "Paris Geller",
    "Logan Huntzberger",
    "Emily Gilmore",
    "Richard Gilmore",
    "Dean Forester",
    "Lane Kim"
]
GILMORE_SHIPS = [
    "Rory Gilmore/Jess Mariano",
    "Luke Danes/Lorelai Gilmore",
    "Rory Gilmore/Logan Huntzberger",
    "Paris Geller/Rory Gilmore"
]


@click.command()
def command():
    click.secho("Hello", fg='red')

    # Create tags
    click.secho("Creating tags...", fg='green')
    with open("fics/management/commands/tags.txt", "r") as f:
        lines = f.readlines()
        for tag in lines:
            _, created = CustomTag.objects.get_or_create(name=tag)
            if created:
                click.secho(f"---Created tag: {tag}")

    tags = CustomTag.objects.all()

    # Create authors
    click.secho("Creating authors...", fg='green')
    # for i in range(30):
    #     author, created = Author.objects.get_or_create(username=fake.user_name(), url=fake.uri())
    #     if created:
    #         click.secho(f"---Created author: {author.username}")

    authors = Author.objects.all()

    # Create fandoms
    click.secho("Creating fandoms...", fg='green')
    for fandom in FANDOMS:
        _, created = Fandom.objects.get_or_create(name=fandom)
        if created:
            click.secho(f"---Created fandom: {fandom}")

    fandoms = Fandom.objects.all()

    # Create ships
    click.secho("Creating ships...", fg='green')
    for ship in HARRY_POTTER_SHIPS + STAR_WARS_SHIPS + SPY_SHIPS + GILMORE_SHIPS:
        _, created = Ship.objects.get_or_create(name=ship)
        if created:
            click.secho(f"---Created ship: {ship}")

    # Create characters
    click.secho("Creating characters...", fg='green')
    for character in HARRY_POTTER_CHARACTERS + STAR_WARS_CHARACTERS + SPY_CHARACTERS + GILMORE_CHARACTERS:
        _, created = Character.objects.get_or_create(name=character)
        if created:
            print(f"---Created character: {character}")

    characters = Character.objects.all()

    click.secho("Creating fics...", fg='green')

    click.secho("Creating Harry Potter fics...", fg='green')
    fandom = fandoms.filter(name__icontains="Harry").first()

    # Get titles
    click.secho("Retrieving titles...", fg='green')
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

        # fic, created =

