"""
grompt add command - Create a new prompt file.
"""

import click
import yaml
from pathlib import Path
from typing import Any, Optional
from grompt.core.prompt import Prompt
from grompt.infrastructure.storage.yaml_loader import YAMLLoader


def load_config() -> dict[str, Any]:
    """Load .grompt config file."""
    config_file = Path.cwd() / ".grompt"
    if not config_file.exists():
        raise FileNotFoundError('Not a grompt project. Run "grompt init" first.')

    with open(config_file, "r") as f:
        result = yaml.safe_load(f)
        return result if result else {}


@click.command()
@click.argument("name")
@click.option("--model", help="Model to use (e.g., gpt-4)")
@click.option("--template", help="Template text")
@click.option("--description", help="Prompt description")
@click.option("--system", help="System message")
@click.option("--dir", "directory", help="Subdirectory to create prompt in")
def add(
    name: str,
    model: Optional[str],
    template: Optional[str],
    description: Optional[str],
    system: Optional[str],
    directory: Optional[str],
) -> None:
    """
    Create a new prompt file.

    Examples:

        # Create minimal prompt
        grompt add my-prompt

        # Create with options
        grompt add code-review --model gpt-4 --template "Review: {{ code }}"

        # Create in subdirectory
        grompt add backend/api-prompt --dir backend
    """
    try:
        config = load_config()
    except FileNotFoundError as e:
        click.echo(click.style(f"Error: {e}", fg="red"))
        return

    # Determine prompts directory
    prompts_dir = Path.cwd() / config.get("prompts_dir", "prompts")

    # Handle subdirectory
    if directory:
        prompts_dir = prompts_dir / directory
        prompts_dir.mkdir(parents=True, exist_ok=True)

    # Extract prompt ID from name (remove .yaml if present)
    prompt_id = name.replace(".yaml", "")

    # Check if prompt already exists
    loader = YAMLLoader(prompts_dir)
    if loader.exists(prompt_id):
        click.echo(click.style(f'Error: Prompt "{prompt_id}" already exists', fg="red"))
        click.echo(f'File: {prompts_dir / f"{prompt_id}.yaml"}')
        return

    # Use provided model or default from config
    prompt_model = model or config.get("default_model", "gpt-4")

    # Create parameters dict
    parameters = {"model": prompt_model}

    # Create prompt with provided options or defaults
    if template:
        # User provided template
        prompt_template = template
    else:
        # Create minimal template
        prompt_template = (
            "# Add your prompt template here\n" "# Use {{ variable_name }} for variables\n"
        )

    # Create Prompt object
    prompt = Prompt(
        id=prompt_id,
        version=1,
        template=prompt_template,
        parameters=parameters,
        system=system,
        description=description,
    )

    try:
        # Save the prompt
        path = loader.save(prompt)

        click.echo(click.style("✓", fg="green") + f" Created {path}")

        if not template:
            click.echo()
            click.echo("Next steps:")
            click.echo(f"  1. Edit the prompt: vim {path}")
            click.echo(f"  2. Commit changes: grompt commit {prompt_id}")

    except Exception as e:
        click.echo(click.style(f"Error: {e}", fg="red"))
        raise click.Abort()
