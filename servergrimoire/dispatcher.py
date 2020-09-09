from importlib import import_module

import click


def dynamic_import(abs_module_path, class_name):
    module_object = import_module(abs_module_path)
    target_class = getattr(module_object, class_name)
    return target_class


@click.group()
@click.option('--c', "-config", help="Path of the config if different from standard",
              default="~\.servergrimoire_config")
def grimoire(c):
    click.echo(c)


@grimoire.command(help="Run the plugin")
@click.option('--c', "-command", help="Command to run. If not insert launch all the commands")
@click.option('--u', "-url", help="On which url launch the command")
def run(c, u):
    click.echo(c)
    click.echo(u)


@grimoire.command(help="Show the stats")
@click.option('--c', "-command", help="Stats to return. If not insert launch all the commands")
@click.option('--u', "-url", help="On which url return the stats")
def stats(c, u):
    click.echo(c)
    click.echo(u)

@grimoire.command(help="Show the hello message")
def hello():
    print("""
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
    """)
