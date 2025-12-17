"""
Prompt validation logic.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from grompt.core.prompt import Prompt
from grompt.core.template import TemplateRenderer


@dataclass
class ValidationResult:
    """Result of prompt validation."""

    valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        """Check if validation passed (no errors)."""
        return self.valid and len(self.errors) == 0


class PromptValidator:
    """Validate prompts for syntax and basic sanity checks."""

    @staticmethod
    def validate_syntax(prompt: Prompt) -> ValidationResult:
        """
        Validate that template syntax is correct.

        Args:
            prompt: The Prompt to validate

        Returns:
            ValidationResult with syntax validation status
        """
        errors = []

        # Check template syntax
        if not TemplateRenderer.validate(prompt.template):
            errors.append("Template has invalid Jinja2 syntax")

        return ValidationResult(valid=len(errors) == 0, errors=errors)

    @staticmethod
    def validate_renders(
        prompt: Prompt, variables: Optional[Dict[str, Any]] = None
    ) -> ValidationResult:
        """
        Validate that template renders without errors.

        Args:
            prompt: The Prompt to validate
            variables: Optional variables to test rendering with

        Returns:
            ValidationResult with rendering validation status
        """
        errors = []
        warnings = []

        # Use empty dict if no variables provided
        test_vars = variables or {}

        try:
            # Try to render
            rendered = prompt.render(**test_vars)

            # Check if output is empty
            if not rendered or not rendered.strip():
                warnings.append("Template renders to empty string")

        except Exception as e:
            errors.append(f"Template rendering failed: {e}")

        return ValidationResult(valid=len(errors) == 0, errors=errors, warnings=warnings)

    @staticmethod
    def validate(prompt: Prompt, variables: Optional[Dict[str, Any]] = None) -> ValidationResult:
        """
        Validate prompt syntax and rendering.

        Args:
            prompt: The Prompt to validate
            variables: Optional variables to test rendering with

        Returns:
            ValidationResult with combined validation status
        """
        # Validate syntax
        syntax_result = PromptValidator.validate_syntax(prompt)

        # Validate rendering
        render_result = PromptValidator.validate_renders(prompt, variables)

        # Combine results
        all_errors = syntax_result.errors + render_result.errors
        all_warnings = render_result.warnings

        return ValidationResult(
            valid=len(all_errors) == 0, errors=all_errors, warnings=all_warnings
        )
