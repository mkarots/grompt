"""
Unit tests for PromptValidator.
"""

from grompt.core.prompt import Prompt
from grompt.core.validator import PromptValidator, ValidationResult


class TestPromptValidator:
    """Test cases for PromptValidator."""

    def test_validate_syntax_valid(self):
        """Test syntax validation passes for valid template."""
        prompt = Prompt(
            id="test", version=1, template="Hello {{ name }}!", parameters={"model": "gpt-4"}
        )
        result = PromptValidator.validate_syntax(prompt)
        assert result.valid is True
        assert len(result.errors) == 0

    def test_validate_syntax_invalid(self):
        """Test syntax validation fails for invalid template."""
        prompt = Prompt(
            id="test", version=1, template="{% if unclosed %}", parameters={"model": "gpt-4"}
        )
        result = PromptValidator.validate_syntax(prompt)
        assert result.valid is False
        assert len(result.errors) > 0
        assert "invalid Jinja2 syntax" in result.errors[0]

    def test_validate_renders_success(self):
        """Test rendering validation passes when template renders."""
        prompt = Prompt(
            id="test", version=1, template="Hello {{ name }}!", parameters={"model": "gpt-4"}
        )
        result = PromptValidator.validate_renders(prompt, {"name": "World"})
        assert result.valid is True
        assert len(result.errors) == 0

    def test_validate_renders_empty_output(self):
        """Test rendering validation warns on empty output."""
        # Use a template that renders to empty string (whitespace only)
        prompt = Prompt(id="test", version=1, template="   ", parameters={"model": "gpt-4"})
        result = PromptValidator.validate_renders(prompt)
        assert result.valid is True
        assert len(result.warnings) > 0
        assert "empty string" in result.warnings[0]

    def test_validate_renders_with_missing_vars(self):
        """Test rendering validation handles missing variables gracefully."""
        prompt = Prompt(
            id="test", version=1, template="Hello {{ name }}!", parameters={"model": "gpt-4"}
        )
        # Missing 'name' variable - Jinja2 renders as empty string
        result = PromptValidator.validate_renders(prompt)
        assert result.valid is True
        # Should render successfully (empty string for undefined vars)

    def test_validate_combined(self):
        """Test combined validation (syntax + rendering)."""
        prompt = Prompt(
            id="test", version=1, template="Hello {{ name }}!", parameters={"model": "gpt-4"}
        )
        result = PromptValidator.validate(prompt, {"name": "World"})
        assert result.valid is True
        assert len(result.errors) == 0

    def test_validate_combined_with_errors(self):
        """Test combined validation catches syntax errors."""
        prompt = Prompt(
            id="test", version=1, template="{% if unclosed %}", parameters={"model": "gpt-4"}
        )
        result = PromptValidator.validate(prompt)
        assert result.valid is False
        assert len(result.errors) > 0

    def test_validation_result_passed(self):
        """Test ValidationResult.passed property."""
        result = ValidationResult(valid=True, errors=[], warnings=[])
        assert result.passed is True

        result = ValidationResult(valid=True, errors=["error"], warnings=[])
        assert result.passed is False

        result = ValidationResult(valid=False, errors=["error"], warnings=[])
        assert result.passed is False
