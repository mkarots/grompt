"""
Hash generation for prompts.
"""

import hashlib
import yaml
from typing import Dict
from grompt.core.prompt import Prompt


class PromptHasher:
    """Generate hashes for prompt content."""

    @staticmethod
    def generate_hash(prompt: Prompt) -> str:
        """
        Generate a SHA256 hash of the prompt content.

        Only hashes the content that matters (id, parameters, template, system).
        Version and metadata are excluded to allow tracking content changes.

        Args:
            prompt: The Prompt object to hash

        Returns:
            First 12 characters of the SHA256 hash (like git)
        """
        # Only hash the content that matters
        content = {
            "id": prompt.id,
            "parameters": prompt.parameters,
            "template": prompt.template,
        }

        # Include system message if present
        if prompt.system:
            content["system"] = prompt.system

        # Create deterministic YAML string
        yaml_str = yaml.dump(content, sort_keys=True, default_flow_style=False)

        # Generate SHA256 hash
        hash_obj = hashlib.sha256(yaml_str.encode("utf-8"))

        # Return first 12 characters (like git)
        return hash_obj.hexdigest()[:12]

    @staticmethod
    def generate_hash_from_dict(data: Dict) -> str:
        """
        Generate a hash from a dictionary.

        Args:
            data: Dictionary containing prompt data

        Returns:
            First 12 characters of the SHA256 hash
        """
        # Handle parameters extraction
        parameters = data.get("parameters", {})
        if "model" in data and "model" not in parameters:
            parameters["model"] = data["model"]

        # Extract only the content that matters
        content = {
            "id": data.get("id"),
            "parameters": parameters,
            "template": data.get("template"),
        }

        # Include system message if present
        if data.get("system"):
            content["system"] = data["system"]

        # Create deterministic YAML string
        yaml_str = yaml.dump(content, sort_keys=True, default_flow_style=False)

        # Generate SHA256 hash
        hash_obj = hashlib.sha256(yaml_str.encode("utf-8"))

        # Return first 12 characters
        return hash_obj.hexdigest()[:12]

    @staticmethod
    def verify_hash(prompt: Prompt) -> bool:
        """
        Verify that the prompt's hash matches its content.

        Args:
            prompt: The Prompt object to verify

        Returns:
            True if hash matches, False otherwise
        """
        if not prompt.hash:
            return False

        expected_hash = PromptHasher.generate_hash(prompt)
        return prompt.hash == expected_hash
