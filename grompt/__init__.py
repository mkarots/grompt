"""
Grompt - Git for Prompts

A simple system to organize, version, and manage LLM prompts separately from code.
"""

from pathlib import Path
from typing import Union

from grompt.core.prompt import Prompt
from grompt.core.template import TemplateRenderer
from grompt.infrastructure.storage.yaml_loader import YAMLLoader
from grompt.utils import load_variables

__version__ = "0.1.0"
__all__ = ["Prompt", "TemplateRenderer", "load", "load_variables"]


def load(
    prompt_id: Union[str, Path], loader: str = "yaml", prompts_dir: Union[str, Path] = "prompts"
) -> Prompt:
    """
    Load a prompt by ID or file path.

    Args:
        prompt_id: The ID of the prompt or path to the prompt file
        loader: The loader type to use (default: "yaml")
        prompts_dir: Directory containing prompts (default: "prompts")

    Returns:
        The loaded Prompt object
    """
    if loader == "yaml":
        prompt_loader = YAMLLoader(prompts_dir=Path(prompts_dir))
        return prompt_loader.load_prompt(str(prompt_id))
    else:
        raise ValueError(f"Unsupported loader type: {loader}")
