from importlib import import_module
import click
from .configmanager import ConfigManager


def dynamic_import(abs_module_path, class_name):
    module_object = import_module(abs_module_path)
    target_class = getattr(module_object, class_name)
    return target_class


@click.group()
@click.pass_context
@click.option('--c', help="Path of the config if different from standard",default="~\.servergrimoire_config")
def grimoire(c):
    hello()
    print("")
    print("For help use --help")
    ConfigManager(c)


@grimoire.command()
@click.pass_context
def sync(ctx):
    click.echo('Debug is %s' % (ctx.obj['DEBUG'] and 'on' or 'off'))

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
