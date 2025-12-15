"""
Grompt - Git for Prompts

A simple system to organize, version, and manage LLM prompts separately from code.
"""

from pathlib import Path
from typing import Optional, Union

from grompt.core.prompt import Prompt
from grompt.core.template import TemplateRenderer
from grompt.infrastructure.storage.yaml_loader import YAMLLoader

__version__ = "0.1.0"
__all__ = ["Prompt", "TemplateRenderer", "load"]


def load(prompt_id: str, loader: str = "yaml", prompts_dir: Union[str, Path] = "prompts") -> Prompt:
    """
    Load a prompt by ID.
    
    Args:
        prompt_id: The ID of the prompt to load
        loader: The loader type to use (default: "yaml")
        prompts_dir: Directory containing prompts (default: "prompts")
        
    Returns:
        The loaded Prompt object
    """
    if loader == "yaml":
        prompt_loader = YAMLLoader(prompts_dir=Path(prompts_dir))
        return prompt_loader.load_prompt(prompt_id)
    else:
        raise ValueError(f"Unsupported loader type: {loader}")
