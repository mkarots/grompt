"""
Execution core for running prompts.
"""

from typing import Protocol, Dict, Any
from grompt.core.prompt import Prompt


class PromptExecutor(Protocol):
    """Interface for executing prompts."""

    def execute(self, prompt: Prompt, inputs: Dict[str, Any]) -> str:
        """
        Execute the prompt with the given inputs.

        The executor should look at prompt.parameters to decide
        how to run (e.g. which model, temperature).
        """
        ...


# Registry for executors
_executors: Dict[str, PromptExecutor] = {}


def register_executor(name: str, executor: PromptExecutor) -> None:
    """Register a new executor."""
    _executors[name] = executor


def get_executor(name: str) -> PromptExecutor:
    """Get a registered executor by name."""
    if name not in _executors:
        raise ValueError(f"No executor registered for '{name}'")
    return _executors[name]
