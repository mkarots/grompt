"""
Core domain logic for Grompt.

This layer contains pure business logic with no external dependencies.
"""

from grompt.core.prompt import Prompt
from grompt.core.template import TemplateRenderer

__all__ = ["Prompt", "TemplateRenderer"]
