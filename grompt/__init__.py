"""
Grompt - Git for Prompts

A simple system to organize, version, and manage LLM prompts separately from code.
"""

from grompt.core.prompt import Prompt
from grompt.core.template import TemplateRenderer

__version__ = "0.1.0"
__all__ = ["Prompt", "TemplateRenderer"]