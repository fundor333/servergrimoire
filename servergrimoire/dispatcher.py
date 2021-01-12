from importlib import import_module

import click

from servergrimoire.app import GrimoirePage


def dynamic_import(abs_module_path, class_name):
    module_object = import_module(abs_module_path)
    target_class = getattr(module_object, class_name)
    return target_class


@click.group()
@click.option(
    "--c",
    "-config",
    help="Path of the config if different from standard",
    default=None,
)
@click.pass_context
def grimoire(ctx, c):
    ctx.obj = GrimoirePage(c)


@grimoire.command(help="Run the command")
@click.option(
    "--c",
    "-command",
    help="Command to run. If not insert launch all the commands",
)
@click.option("--u", "-url", help="On which url launch the command")
@click.option(
    "--stats/--no-stats", default=False, help="Launch stats after the run"
)
@click.pass_context
def run(ctx, c, u, stats):
    ctx.obj.run(c, u)
    if stats:
        ctx.obj.stats(c, u)


@grimoire.command(help="Show the stats")
@click.option(
    "--c",
    "-command",
    help="Stats to return. If not insert launch all the commands",
)
@click.option("--u", "-url", help="On which url return the stats")
@click.option("--s", "-short", is_flag=True, help="Short version of the stats")
@click.pass_context
def stats(ctx, c, u, s):
    ctx.obj.stats(c, u, s)


@grimoire.command(help="Show the info")
@click.option("--u", "-url", help="On which url return the info")
@click.option("--c", "-command", help="On which directive return the info")
@click.pass_context
def info(ctx, c, u):
    ctx.obj.info(command=c, url=u)


@grimoire.command(help="Add the url to the command check")
@click.option("--u", "-url", help="Url to add", multiple=True)
@click.pass_context
def add(ctx, u):
    ctx.obj.add(url=u)


@grimoire.command(help="Remove the url to the command check")
@click.option("--u", "-url", help="Url to remove")
@click.pass_context
def remove(ctx, u):
    ctx.obj.remove(u)


@grimoire.command(help="Show the hello message")
def hello():
    print(
        """
.d8888b.
d88P  Y88b
Y88b.
 "Y888b.    .d88b.  888d888 888  888  .d88b.  888d888
    "Y88b. d8P  Y8b 888P"   888  888 d8P  Y8b 888P"
      "888 88888888 888     Y88  88P 88888888 888
Y88b  d88P Y8b.     888      Y8bd8P  Y8b.     888
 "Y8888P"   "Y8888  888       Y88P    "Y8888  888



 .d8888b.          d8b                        d8b
d88P  Y88b         Y8P                        Y8P
888    888
888        888d888 888 88888b.d88b.   .d88b.  888 888d888 .d88b.
888  88888 888P"   888 888 "888 "88b d88""88b 888 888P"  d8P  Y8b
888    888 888     888 888  888  888 888  888 888 888    88888888
Y88b  d88P 888     888 888  888  888 Y88..88P 888 888    Y8b.
 "Y8888P88 888     888 888  888  888  "Y88P"  888 888     "Y8888
    """
    )
