"""
Core Prompt entity - pure domain model.
"""

from dataclasses import dataclass, field
from typing import Dict, Optional, Any


@dataclass
class Prompt:
    """
    Core Prompt entity representing an LLM prompt.

    This is a pure domain model with no external dependencies.
    """

    id: str
    version: int
    template: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    hash: Optional[str] = None
    system: Optional[str] = None
    description: Optional[str] = None
    variables: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate prompt data after initialization."""
        if not self.id:
            raise ValueError("Prompt ID cannot be empty")
        if self.version < 1:
            raise ValueError("Prompt version must be >= 1")
        if not self.template:
            raise ValueError("Prompt template cannot be empty")
        if not isinstance(self.parameters, dict):
            self.parameters = {}

    @property
    def model(self) -> Optional[str]:
        """Backward compatibility helper to get model from parameters."""
        return self.parameters.get("model")

    def to_dict(self) -> Dict[str, Any]:
        """Convert prompt to dictionary for serialization."""
        data = {
            "id": self.id,
            "version": self.version,
            "template": self.template,
            "parameters": self.parameters,
        }

        if self.hash:
            data["hash"] = self.hash
        if self.system:
            data["system"] = self.system
        if self.description:
            data["description"] = self.description
        if self.variables:
            data["variables"] = self.variables

        # Add any additional metadata
        data.update(self.metadata)

        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Prompt":
        """Create a Prompt from a dictionary."""
        # Extract known fields
        prompt_id = data.get("id", "")
        version = data.get("version", 1)
        template = data.get("template", "")

        # Handle parameters / legacy model field
        parameters = data.get("parameters", {})
        if "model" in data and "model" not in parameters:
            parameters["model"] = data["model"]

        prompt_hash = data.get("hash")
        system = data.get("system")
        description = data.get("description")
        variables = data.get("variables", {})

        # Everything else goes into metadata
        metadata_keys = {
            "id",
            "version",
            "model",
            "template",
            "hash",
            "system",
            "description",
            "variables",
            "parameters",
        }
        metadata = {k: v for k, v in data.items() if k not in metadata_keys}

        return cls(
            id=prompt_id,
            version=version,
            template=template,
            parameters=parameters,
            hash=prompt_hash,
            system=system,
            description=description,
            variables=variables,
            metadata=metadata,
        )

    def render(self, **kwargs: Any) -> str:
        """
        Render the prompt template with the provided variables.

        Args:
            **kwargs: Variables to pass to the template

        Returns:
            The rendered template string
        """
        from grompt.core.template import TemplateRenderer

        return TemplateRenderer.render(self.template, **kwargs)
