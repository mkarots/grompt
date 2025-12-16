"""
grompt commit command - Version and hash a prompt.
"""

import click
import yaml
from pathlib import Path
from typing import Any, Optional
from grompt.infrastructure.storage.yaml_loader import YAMLLoader
from grompt.infrastructure.storage.hasher import PromptHasher


def load_config() -> dict[str, Any]:
    """Load .grompt config file."""
    config_file = Path.cwd() / '.grompt'
    if not config_file.exists():
        raise FileNotFoundError(
            'Not a grompt project. Run "grompt init" first.'
        )
    
    with open(config_file, 'r') as f:
        result = yaml.safe_load(f)
        return result if result else {}


@click.command()
@click.argument('name')
@click.argument('message', required=False)
def commit(name: str, message: Optional[str]) -> None:
    """
    Commit changes to a prompt (increment version and generate hash).
    
    Examples:
    
        # Basic commit
        grompt commit my-prompt
        
        # Commit with message
        grompt commit my-prompt "Optimized for fewer tokens"
    """
    try:
        config = load_config()
    except FileNotFoundError as e:
        click.echo(click.style(f'Error: {e}', fg='red'))
        return
    
    # Determine prompts directory
    prompts_dir = Path.cwd() / config.get('prompts_dir', 'prompts')
    
    # Extract prompt ID from name
    prompt_id = name.replace('.yaml', '')
    
    # Load the prompt
    loader = YAMLLoader(prompts_dir)
    
    if not loader.exists(prompt_id):
        click.echo(click.style(f'Error: Prompt "{prompt_id}" not found', fg='red'))
        click.echo(f'Expected file: {prompts_dir / f"{prompt_id}.yaml"}')
        return
    
    try:
        # Load current prompt
        prompt = loader.load_prompt(prompt_id)
        
        # Store old version
        old_version = prompt.version
        old_hash = prompt.hash
        
        # Increment version
        prompt.version += 1
        
        # Generate new hash
        new_hash = PromptHasher.generate_hash(prompt)
        prompt.hash = new_hash
        
        # Save updated prompt
        _ = loader.save(prompt)
        
        # Display results
        click.echo(click.style('✓', fg='green') + f' Committed {prompt_id}')
        click.echo(f'  version: {old_version} → {prompt.version}')
        
        if old_hash:
            click.echo(f'  hash: {old_hash} → {new_hash}')
        else:
            click.echo(f'  hash: {new_hash}')
        
        if message:
            click.echo(f'  message: {message}')
        
        # TODO: Optionally save to history file
        # This could be implemented later to track all commits
        
    except Exception as e:
        click.echo(click.style(f'Error: {e}', fg='red'))
        raise click.Abort()