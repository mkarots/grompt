"""
Unit tests for the TemplateRenderer service.
"""

import pytest
from jinja2 import TemplateError
from grompt.core.template import TemplateRenderer


class TestTemplateRenderer:
    """Test cases for the TemplateRenderer class."""

    def test_render_simple_variable(self):
        """Test rendering a simple string variable."""
        template = "Hello {{ name }}!"
        result = TemplateRenderer.render(template, name="World")
        assert result == "Hello World!"

    def test_render_multiple_variables(self):
        """Test rendering multiple variables."""
        template = "{{ greeting }} {{ name }}."
        result = TemplateRenderer.render(template, greeting="Hi", name="Alice")
        assert result == "Hi Alice."

    def test_render_loops(self):
        """Test rendering a loop."""
        template = "{% for item in items %}- {{ item }}\n{% endfor %}"
        result = TemplateRenderer.render(template, items=["a", "b"])
        assert "- a" in result
        assert "- b" in result

    def test_render_conditionals(self):
        """Test rendering conditionals."""
        template = "{% if show %}Visible{% else %}Hidden{% endif %}"
        assert TemplateRenderer.render(template, show=True) == "Visible"
        assert TemplateRenderer.render(template, show=False) == "Hidden"

    def test_render_raises_error_on_syntax(self):
        """Test that rendering raises TemplateError on invalid syntax."""
        template = "{% if unclosed %}"
        with pytest.raises(TemplateError, match="Failed to render template"):
            TemplateRenderer.render(template)

    def test_render_undefined_variables(self):
        """
        Test behavior with undefined variables.
        Jinja2 by default returns empty string for undefined variables.
        """
        template = "Hello {{ missing }}!"
        result = TemplateRenderer.render(template)
        assert result == "Hello !"

    def test_validate_valid_template(self):
        """Test validation returns True for valid templates."""
        assert TemplateRenderer.validate("Hello {{ name }}") is True
        assert TemplateRenderer.validate("{% if x %}y{% endif %}") is True

    def test_validate_invalid_template(self):
        """Test validation returns False for invalid templates."""
        assert TemplateRenderer.validate("{% if unclosed %}") is False
        assert TemplateRenderer.validate("{{ unclosed_variable") is False
