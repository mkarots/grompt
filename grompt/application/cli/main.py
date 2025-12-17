"""
Main CLI entry point for Grompt.
"""

import click
from grompt.application.cli.commands import init, add, commit


@click.group()
@click.version_option(version="0.1.0")
def cli() -> None:
    """
    Grompt - Git for Prompts

    Manage LLM prompts with version control.
    """
    pass


# Register commands
cli.add_command(init.init)
cli.add_command(add.add)
cli.add_command(commit.commit)


if __name__ == "__main__":
    cli()
