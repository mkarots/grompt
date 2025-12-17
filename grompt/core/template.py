"""
Template rendering logic using Jinja2.
"""

from typing import Any
from jinja2 import Template, TemplateError


class TemplateRenderer:
    """Pure template rendering logic."""

    @staticmethod
    def render(template: str, **kwargs: Any) -> str:
        """
        Render a Jinja2 template with variables.

        Args:
            template: The Jinja2 template string
            **kwargs: Variables to pass to the template

        Returns:
            The rendered template string

        Raises:
            TemplateError: If template rendering fails
        """
        try:
            t = Template(template)
            return t.render(**kwargs)
        except TemplateError as e:
            raise TemplateError(f"Failed to render template: {e}") from e

    @staticmethod
    def validate(template: str) -> bool:
        """
        Validate that a template string is valid Jinja2.

        Args:
            template: The template string to validate

        Returns:
            True if valid, False otherwise
        """
        try:
            Template(template)
            return True
        except TemplateError:
            return False
