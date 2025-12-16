"""
Unit tests for the Prompt core entity.
"""

import pytest
from grompt.core.prompt import Prompt
from jinja2 import TemplateError

class TestPrompt:
    """Test cases for the Prompt class."""

    def test_init_happy_path(self):
        """Test successful initialization with required fields."""
        prompt = Prompt(
            id="test-prompt",
            version=1,
            template="Hello {{ name }}!",
            parameters={"model": "gpt-4"}
        )
        assert prompt.id == "test-prompt"
        assert prompt.version == 1
        assert prompt.template == "Hello {{ name }}!"
        assert prompt.parameters["model"] == "gpt-4"
        assert prompt.model == "gpt-4"  # Check property accessor
        assert prompt.variables == {}
        assert prompt.metadata == {}

    def test_init_full_fields(self):
        """Test initialization with all fields."""
        prompt = Prompt(
            id="complex-prompt",
            version=2,
            template="Result: {{ result }}",
            parameters={"model": "gpt-3.5", "temp": 0.7},
            hash="abc123hash",
            system="You are a helper.",
            description="A complex prompt",
            variables={"result": {"type": "string"}},
            metadata={"custom_tag": "beta"}
        )
        assert prompt.hash == "abc123hash"
        assert prompt.system == "You are a helper."
        assert prompt.description == "A complex prompt"
        assert prompt.variables["result"]["type"] == "string"
        assert prompt.metadata["custom_tag"] == "beta"
        assert prompt.parameters["temp"] == 0.7

    def test_validation_empty_id(self):
        """Test validation fails with empty ID."""
        with pytest.raises(ValueError, match="Prompt ID cannot be empty"):
            Prompt(id="", version=1, template="t")

    def test_validation_invalid_version(self):
        """Test validation fails with version < 1."""
        with pytest.raises(ValueError, match="Prompt version must be >= 1"):
            Prompt(id="test", version=0, template="t")

    def test_validation_empty_template(self):
        """Test validation fails with empty template."""
        with pytest.raises(ValueError, match="Prompt template cannot be empty"):
            Prompt(id="test", version=1, template="")
            
    def test_parameters_default(self):
        """Test parameters defaults to empty dict."""
        prompt = Prompt(id="test", version=1, template="t")
        assert prompt.parameters == {}

    def test_to_dict(self):
        """Test serialization to dictionary."""
        prompt = Prompt(
            id="serialize-me",
            version=1,
            template="Template",
            parameters={"model": "gpt-4"},
            system="System",
            metadata={"extra": "value"}
        )
        data = prompt.to_dict()
        
        assert data["id"] == "serialize-me"
        assert data["version"] == 1
        assert data["parameters"]["model"] == "gpt-4"
        assert data["template"] == "Template"
        assert data["system"] == "System"
        assert data["extra"] == "value"
        assert "hash" not in data

    def test_from_dict_basic(self):
        """Test deserialization from minimal dictionary."""
        data = {
            "id": "deserialize-me",
            "parameters": {"model": "gpt-4"},
            "template": "Template Content"
        }
        # version defaults to 1
        prompt = Prompt.from_dict(data)
        
        assert prompt.id == "deserialize-me"
        assert prompt.version == 1
        assert prompt.model == "gpt-4"
        assert prompt.template == "Template Content"

    def test_from_dict_legacy_model(self):
        """Test deserialization from legacy dict with top-level model field."""
        data = {
            "id": "legacy",
            "model": "gpt-3.5",
            "template": "Old"
        }
        prompt = Prompt.from_dict(data)
        assert prompt.model == "gpt-3.5"
        assert prompt.parameters["model"] == "gpt-3.5"

    def test_from_dict_full_with_metadata(self):
        """Test deserialization handling metadata."""
        data = {
            "id": "meta-prompt",
            "version": 5,
            "parameters": {"model": "claude-2"},
            "template": "Hi",
            "extra_field_1": "value1",
            "extra_field_2": 123
        }
        prompt = Prompt.from_dict(data)
        
        assert prompt.id == "meta-prompt"
        assert prompt.metadata["extra_field_1"] == "value1"
        assert prompt.metadata["extra_field_2"] == 123
        # Ensure known fields are not in metadata
        assert "id" not in prompt.metadata

    def test_render_delegation(self):
        """Test that render method correctly delegates to TemplateRenderer."""
        prompt = Prompt(
            id="render-test",
            version=1,
            template="Hello {{ name }}!"
        )
        result = prompt.render(name="World")
        assert result == "Hello World!"

    def test_render_error(self):
        """Test that render raises TemplateError on bad template logic."""
        prompt = Prompt(
            id="bad-render",
            version=1,
            template="{% if missing_end %}"
        )
        with pytest.raises(TemplateError):
            prompt.render()
