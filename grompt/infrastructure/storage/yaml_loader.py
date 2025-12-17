"""
YAML file loader for prompts.
"""

import yaml
from pathlib import Path
from typing import Any, Optional
from grompt.core.prompt import Prompt


class YAMLLoader:
    """Adapter for loading and saving YAML prompt files."""

    def __init__(self, prompts_dir: Path = Path("prompts")):
        """
        Initialize the YAML loader.

        Args:
            prompts_dir: Directory where prompt files are stored
        """
        self.prompts_dir = Path(prompts_dir)

    def _resolve_path(self, prompt_id: str) -> Path:
        """Resolve prompt ID to a file path."""
        path = Path(prompt_id)

        # Check if it's a direct file path (absolute or relative)
        if path.suffix.lower() in (".yaml", ".yml") and path.exists():
            return path

        # Default to prompts directory
        return self.prompts_dir / f"{prompt_id}.yaml"

    def load(self, prompt_id: str) -> dict[str, Any]:
        """
        Load a prompt YAML file.

        Args:
            prompt_id: The prompt ID (filename without .yaml) or a file path

        Returns:
            Dictionary containing the prompt data

        Raises:
            FileNotFoundError: If the prompt file doesn't exist
            yaml.YAMLError: If the YAML is invalid
        """
        path = self._resolve_path(prompt_id)

        if not path.exists():
            raise FileNotFoundError(f"Prompt file not found: {path}")

        with open(path, "r") as f:
            data = yaml.safe_load(f)

        if not data:
            raise ValueError(f"Empty or invalid YAML file: {path}")

        return dict(data)

    def save(self, prompt: Prompt, prompt_id: Optional[str] = None) -> Path:
        """
        Save a prompt to a YAML file.

        Args:
            prompt: The Prompt object to save
            prompt_id: Optional custom filename (defaults to prompt.id)

        Returns:
            Path to the saved file
        """
        filename = prompt_id or prompt.id
        path = self.prompts_dir / f"{filename}.yaml"

        # Create directory if it doesn't exist
        path.parent.mkdir(parents=True, exist_ok=True)

        # Convert prompt to dict and save
        data = prompt.to_dict()

        with open(path, "w") as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)

        return path

    def load_prompt(self, prompt_id: str) -> Prompt:
        """
        Load a prompt file and return a Prompt object.

        Args:
            prompt_id: The prompt ID

        Returns:
            Prompt object
        """
        data = self.load(prompt_id)
        return Prompt.from_dict(data)

    def exists(self, prompt_id: str) -> bool:
        """
        Check if a prompt file exists.

        Args:
            prompt_id: The prompt ID or file path

        Returns:
            True if the file exists, False otherwise
        """
        return self._resolve_path(prompt_id).exists()

    def list_prompts(self) -> list[str]:
        """
        List all prompt IDs in the prompts directory.

        Returns:
            List of prompt IDs (filenames without .yaml extension)
        """
        if not self.prompts_dir.exists():
            return []

        return [p.stem for p in self.prompts_dir.glob("**/*.yaml") if p.is_file()]
