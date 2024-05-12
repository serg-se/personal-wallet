import click

from personal_wallet import commands

__version__ = "0.1.0"


@click.version_option(prog_name="personal_wallet", version=__version__)
@click.group()
def main():
    pass


main.add_command(commands.balance)
main.add_command(commands.add)
main.add_command(commands.find)
main.add_command(commands.update)
main.add_command(commands.delete)
