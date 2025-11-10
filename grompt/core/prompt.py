"""
Core Prompt entity - pure domain model.
"""

from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class Prompt:
    """
    Core Prompt entity representing an LLM prompt.
    
    This is a pure domain model with no external dependencies.
    """
    
    id: str
    version: int
    model: str
    template: str
    hash: Optional[str] = None
    system: Optional[str] = None
    description: Optional[str] = None
    variables: Dict[str, any] = field(default_factory=dict)
    metadata: Dict[str, any] = field(default_factory=dict)
    
    def __post_init__(self) -> None:
        """Validate prompt data after initialization."""
        if not self.id:
            raise ValueError("Prompt ID cannot be empty")
        if self.version < 1:
            raise ValueError("Prompt version must be >= 1")
        if not self.model:
            raise ValueError("Prompt model cannot be empty")
        if not self.template:
            raise ValueError("Prompt template cannot be empty")
    
    def to_dict(self) -> Dict[str, any]:
        """Convert prompt to dictionary for serialization."""
        data = {
            "id": self.id,
            "version": self.version,
            "model": self.model,
            "template": self.template,
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
    def from_dict(cls, data: Dict[str, any]) -> "Prompt":
        """Create a Prompt from a dictionary."""
        # Extract known fields
        id = data.get("id")
        version = data.get("version", 1)
        model = data.get("model", "gpt-4")
        template = data.get("template", "")
        hash = data.get("hash")
        system = data.get("system")
        description = data.get("description")
        variables = data.get("variables", {})
        
        # Everything else goes into metadata
        metadata_keys = {"id", "version", "model", "template", "hash", "system", "description", "variables"}
        metadata = {k: v for k, v in data.items() if k not in metadata_keys}
        
        return cls(
            id=id,
            version=version,
            model=model,
            template=template,
            hash=hash,
            system=system,
            description=description,
            variables=variables,
            metadata=metadata,
        )