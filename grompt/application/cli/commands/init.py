"""
grompt init command - Initialize a grompt project.
"""

import click
import yaml
from pathlib import Path


@click.command()
@click.option(
    "--prompts-dir", default="prompts", help="Directory for prompt files (default: prompts)"
)
@click.option("--model", default="gpt-4", help="Default model (default: gpt-4)")
def init(prompts_dir: str, model: str) -> None:
    """
    Initialize a grompt project in the current directory.

    Creates:
    - .grompt config file
    - prompts/ directory
    """
    cwd = Path.cwd()
    config_file = cwd / ".grompt"
    prompts_path = cwd / prompts_dir

    # Check if already initialized
    if config_file.exists():
        click.echo(click.style("Error: Grompt project already initialized", fg="red"))
        click.echo(f"Config file exists: {config_file}")
        return

    # Create config
    config = {
        "version": 1,
        "prompts_dir": prompts_dir,
        "default_model": model,
    }

    try:
        # Write config file
        with open(config_file, "w") as f:
            yaml.dump(config, f, default_flow_style=False)

        click.echo(click.style("✓", fg="green") + " Created .grompt")

        # Create prompts directory
        prompts_path.mkdir(parents=True, exist_ok=True)
        click.echo(click.style("✓", fg="green") + f" Created {prompts_dir}/ directory")

        click.echo()
        click.echo(click.style("Grompt project initialized!", fg="green", bold=True))
        click.echo()
        click.echo("Next steps:")
        click.echo("  1. Create a prompt: grompt add my-prompt")
        click.echo(f"  2. Edit it: vim {prompts_dir}/my-prompt.yaml")
        click.echo("  3. Commit changes: grompt commit my-prompt")

    except Exception as e:
        click.echo(click.style(f"Error: {e}", fg="red"))
        raise click.Abort()
