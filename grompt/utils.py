"""
Utility functions for working with prompts.
Optional helpers - not required for core functionality.
"""

from pathlib import Path
from typing import Dict, Any, Union
import yaml


def load_variables(file_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Load variables from a YAML file.

    Users can organize files however they want - this function
    doesn't enforce any structure. Just loads YAML and returns
    the dictionary of variables.

    Args:
        file_path: Path to YAML file (relative or absolute).
                   Supports file:// URI format (optional).

    Returns:
        Dictionary of variables to pass to prompt.render()

    Raises:
        FileNotFoundError: If file doesn't exist
        yaml.YAMLError: If YAML is invalid

    Example:
        >>> variables = load_variables("inputs/simple.yaml")
        >>> prompt.render(**variables)
    """
    path = Path(file_path)

    # Handle file:// URI (optional sugar)
    if isinstance(file_path, str) and file_path.startswith("file://"):
        path = Path(file_path[7:])

    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    with open(path, "r") as f:
        data = yaml.safe_load(f)

    # Return empty dict if file is empty or None
    return data or {}
