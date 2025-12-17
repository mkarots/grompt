# Grompt Coding Guidelines

This document defines the coding standards and architectural patterns for the Grompt project. Use this as a reference when contributing code or when configuring your IDE/Claude to maintain consistency.

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Code Style](#code-style)
3. [Type Hints](#type-hints)
4. [Documentation](#documentation)
5. [Testing](#testing)
6. [Layer Rules](#layer-rules)
7. [Naming Conventions](#naming-conventions)
8. [Error Handling](#error-handling)
9. [Dependencies](#dependencies)

---

## Architecture Overview

Grompt follows **Clean Architecture** with three main layers:

```
Application Layer (CLI, Public API)
    ↓ depends on
Core Layer (Pure domain logic)
    ↑ depends on
Infrastructure Layer (External adapters)
```

### Layer Responsibilities

- **Core**: Pure business logic, no I/O, no external dependencies (except allowed: Jinja2)
- **Infrastructure**: Adapters for external systems (file I/O, hashing)
- **Application**: Orchestrates Core + Infrastructure (CLI commands, public API)
- **Utils**: Optional helpers with no dependencies (standalone utilities)

---

## Code Style

### Formatting

- **Line Length**: 100 characters (configured in `pyproject.toml`)
- **Formatter**: Black (run `black grompt/ tests/`)
- **Linter**: Ruff (run `ruff check grompt/ tests/`)
- **Type Checker**: MyPy (run `mypy grompt/`)

### Python Version

- **Minimum**: Python 3.9
- **Target Versions**: 3.9, 3.10, 3.11, 3.12

### Code Style Rules

```python
# ✅ GOOD: Clear, descriptive names
def load_prompt_by_id(prompt_id: str) -> Prompt:
    """Load a prompt by its ID."""
    ...

# ❌ BAD: Abbreviated, unclear
def ld_prmpt(id: str) -> Prompt:
    ...

# ✅ GOOD: Type hints on all functions
def render_template(template: str, **kwargs: Any) -> str:
    ...

# ❌ BAD: Missing type hints
def render_template(template, **kwargs):
    ...

# ✅ GOOD: Docstrings for public APIs
class PromptValidator:
    """Validate prompts for syntax and basic sanity checks."""
    
    @staticmethod
    def validate(prompt: Prompt) -> ValidationResult:
        """Validate prompt syntax and rendering."""
        ...

# ❌ BAD: Missing docstrings
class PromptValidator:
    def validate(prompt):
        ...
```

---

## Type Hints

### Required

- **All function parameters** must have type hints
- **All return values** must have type hints
- **Class attributes** should have type hints (use `dataclass` or annotations)

### Type Hint Style

```python
# ✅ GOOD: Use typing module for complex types
from typing import Dict, List, Optional, Any, Union

def process_data(
    items: List[str],
    metadata: Dict[str, Any],
    count: Optional[int] = None
) -> Union[str, None]:
    ...

# ✅ GOOD: Use built-in types (Python 3.9+)
def process_data(
    items: list[str],
    metadata: dict[str, Any],
    count: int | None = None
) -> str | None:
    ...

# ✅ GOOD: Use Path from pathlib
from pathlib import Path

def load_file(file_path: Path | str) -> str:
    ...

# ❌ BAD: Missing type hints
def process_data(items, metadata, count=None):
    ...
```

### MyPy Configuration

- **Strict Mode**: Enabled (`disallow_untyped_defs = true`)
- **Python Version**: 3.9
- **Warnings**: `warn_return_any = true`, `warn_unused_configs = true`

---

## Documentation

### Docstring Format

Use Google-style docstrings:

```python
def load_prompt(prompt_id: str, prompts_dir: Path = Path("prompts")) -> Prompt:
    """
    Load a prompt by ID from the prompts directory.
    
    Args:
        prompt_id: The prompt ID (filename without .yaml extension)
        prompts_dir: Directory containing prompt files (default: "prompts")
        
    Returns:
        The loaded Prompt object
        
    Raises:
        FileNotFoundError: If the prompt file doesn't exist
        yaml.YAMLError: If the YAML is invalid
        
    Example:
        >>> prompt = load_prompt("code-review")
        >>> print(prompt.template)
    """
    ...
```

### Module Docstrings

Every module should start with a docstring:

```python
"""
YAML file loader for prompts.

This module provides the YAMLLoader class for loading and saving
prompt files in YAML format.
"""
```

### Class Docstrings

```python
class PromptValidator:
    """
    Validate prompts for syntax and basic sanity checks.
    
    This class provides static methods for validating prompt templates,
    ensuring they have valid Jinja2 syntax and can render successfully.
    """
    ...
```

---

## Testing

### Test Structure

- **Location**: `tests/` directory mirrors `grompt/` structure
- **Naming**: `test_*.py` files, `Test*` classes, `test_*` functions
- **Framework**: pytest

### Test Example

```python
"""
Unit tests for PromptValidator.
"""

import pytest
from grompt.core.prompt import Prompt
from grompt.core.validator import PromptValidator


class TestPromptValidator:
    """Test cases for PromptValidator."""

    def test_validate_syntax_valid(self):
        """Test syntax validation passes for valid template."""
        prompt = Prompt(
            id="test",
            version=1,
            template="Hello {{ name }}!",
            parameters={"model": "gpt-4"}
        )
        result = PromptValidator.validate_syntax(prompt)
        assert result.valid is True
        assert len(result.errors) == 0

    def test_validate_syntax_invalid(self):
        """Test syntax validation fails for invalid template."""
        prompt = Prompt(
            id="test",
            version=1,
            template="{% if unclosed %}",
            parameters={"model": "gpt-4"}
        )
        result = PromptValidator.validate_syntax(prompt)
        assert result.valid is False
        assert len(result.errors) > 0
```

### Test Requirements

- **Coverage**: Aim for high coverage (>80%)
- **Independence**: Tests should be independent (no shared state)
- **Naming**: Descriptive test names that explain what's being tested
- **Fixtures**: Use pytest fixtures for common setup

---

## Layer Rules

### Core Layer Rules

```python
# ✅ GOOD: Pure functions, no I/O
class TemplateRenderer:
    @staticmethod
    def render(template: str, **kwargs: Any) -> str:
        """Pure rendering logic."""
        t = Template(template)
        return t.render(**kwargs)

# ❌ BAD: I/O in Core layer
class TemplateRenderer:
    @staticmethod
    def render_from_file(file_path: Path) -> str:  # NO I/O in Core!
        with open(file_path) as f:  # ❌
            ...

# ✅ GOOD: Allowed dependency (Jinja2)
from jinja2 import Template  # ✅ Allowed in Core

# ❌ BAD: Infrastructure dependency in Core
from grompt.infrastructure.storage.yaml_loader import YAMLLoader  # ❌
```

**Core Layer Checklist:**
- ✅ No file I/O
- ✅ No network calls
- ✅ No database access
- ✅ No external system calls
- ✅ Only allowed dependency: Jinja2 (for templates)
- ✅ Pure functions (same input → same output)
- ✅ No mutable global state

### Infrastructure Layer Rules

```python
# ✅ GOOD: Depends only on Core
from grompt.core.prompt import Prompt  # ✅

class YAMLLoader:
    def load_prompt(self, prompt_id: str) -> Prompt:
        # Load from file, return Core entity
        ...

# ❌ BAD: Infrastructure depending on Application
from grompt.application.cli.commands import commit  # ❌
```

**Infrastructure Layer Checklist:**
- ✅ Can depend on Core layer
- ✅ Can do I/O (file, network, database)
- ✅ Implements adapters for external systems
- ✅ Returns Core entities (Prompt, etc.)
- ❌ Cannot depend on Application layer

### Application Layer Rules

```python
# ✅ GOOD: Orchestrates Core + Infrastructure
from grompt.core.prompt import Prompt  # ✅
from grompt.infrastructure.storage.yaml_loader import YAMLLoader  # ✅

def load(prompt_id: str) -> Prompt:
    loader = YAMLLoader()
    return loader.load_prompt(prompt_id)

# ❌ BAD: Business logic in Application
def load(prompt_id: str) -> Prompt:
    # Complex validation logic here ❌
    # Should be in Core layer!
    ...
```

**Application Layer Checklist:**
- ✅ Can depend on Core + Infrastructure
- ✅ Orchestrates use cases
- ✅ Handles user input/output (CLI)
- ✅ No business logic (delegate to Core)
- ❌ Cannot be imported by Core or Infrastructure

---

## Naming Conventions

### Files and Modules

- **Modules**: `snake_case.py` (e.g., `yaml_loader.py`, `prompt_validator.py`)
- **Packages**: `snake_case/` (e.g., `application/cli/commands/`)

### Classes

- **Classes**: `PascalCase` (e.g., `PromptValidator`, `YAMLLoader`)
- **Protocols**: `PascalCase` with descriptive name (e.g., `PromptExecutor`)

### Functions and Methods

- **Functions**: `snake_case` (e.g., `load_prompt`, `validate_syntax`)
- **Private methods**: `_leading_underscore` (e.g., `_resolve_path`)
- **Static methods**: Same as functions, use `@staticmethod`

### Variables

- **Variables**: `snake_case` (e.g., `prompt_id`, `template_str`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `DEFAULT_MODEL`)
- **Private variables**: `_leading_underscore` (e.g., `_executors`)

### Type Variables

- **Type variables**: `PascalCase` (e.g., `T`, `Key`, `Value`)

### Examples

```python
# ✅ GOOD: Clear naming
class PromptValidator:
    DEFAULT_TIMEOUT: int = 30
    
    def validate_syntax(self, prompt: Prompt) -> ValidationResult:
        template_str: str = prompt.template
        _internal_cache: dict[str, Any] = {}
        ...

# ❌ BAD: Unclear naming
class PV:
    T: int = 30
    
    def v(self, p: Prompt) -> VR:
        ts: str = p.template
        ...
```

---

## Error Handling

### Exception Types

```python
# ✅ GOOD: Use specific exceptions
def load_prompt(prompt_id: str) -> Prompt:
    if not path.exists():
        raise FileNotFoundError(f"Prompt not found: {prompt_id}")
    
    try:
        data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Invalid YAML: {e}") from e

# ❌ BAD: Generic exceptions
def load_prompt(prompt_id: str) -> Prompt:
    if not path.exists():
        raise Exception("Error")  # ❌ Too generic
```

### Error Messages

- **Be specific**: Include context (what failed, why)
- **Be actionable**: Tell user what to do
- **Include values**: Show the problematic value when safe

```python
# ✅ GOOD: Specific, actionable
raise ValueError(f"Prompt version must be >= 1, got {version}")

# ❌ BAD: Vague
raise ValueError("Invalid version")
```

### Exception Chaining

```python
# ✅ GOOD: Chain exceptions
try:
    template = Template(template_str)
except TemplateError as e:
    raise TemplateError(f"Failed to render template: {e}") from e

# ❌ BAD: Lose original exception
try:
    template = Template(template_str)
except TemplateError:
    raise TemplateError("Failed")  # ❌ Lost original error
```

---

## Dependencies

### Allowed Dependencies by Layer

#### Core Layer
- ✅ `jinja2` - Template rendering (required)
- ✅ Standard library only (dataclasses, typing, etc.)

#### Infrastructure Layer
- ✅ `pyyaml` - YAML parsing
- ✅ `hashlib` - Hashing (standard library)
- ✅ Core layer entities

#### Application Layer
- ✅ `click` - CLI framework
- ✅ Core + Infrastructure layers

#### Utils Layer
- ✅ `pyyaml` - YAML parsing
- ✅ `pathlib` - Path handling (standard library)
- ❌ No other dependencies

### Adding New Dependencies

1. **Check if it's necessary**: Can we use standard library?
2. **Check layer rules**: Is it allowed in that layer?
3. **Update `pyproject.toml`**: Add to `dependencies` or `[project.optional-dependencies]`
4. **Document why**: Add comment explaining the dependency

---

## Code Examples

### Core Layer Example

```python
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
    
    def __post_init__(self) -> None:
        """Validate prompt data after initialization."""
        if not self.id:
            raise ValueError("Prompt ID cannot be empty")
        if self.version < 1:
            raise ValueError("Prompt version must be >= 1")
        if not self.template:
            raise ValueError("Prompt template cannot be empty")
    
    def render(self, **kwargs: Any) -> str:
        """
        Render the template with given variables.
        
        Args:
            **kwargs: Variables to pass to the template
            
        Returns:
            Rendered template string
        """
        from grompt.core.template import TemplateRenderer
        return TemplateRenderer.render(self.template, **kwargs)
```

### Infrastructure Layer Example

```python
"""
YAML file loader for prompts.
"""

import yaml
from pathlib import Path
from typing import Any
from grompt.core.prompt import Prompt


class YAMLLoader:
    """Adapter for loading and saving YAML prompt files."""
    
    def __init__(self, prompts_dir: Path = Path("prompts")):
        """
        Initialize the YAML loader.
        
        Args:
            prompts_dir: Directory where prompt files are stored
        """
        self.prompts_dir = Path(prompts_dir)
    
    def load_prompt(self, prompt_id: str) -> Prompt:
        """
        Load a prompt by ID.
        
        Args:
            prompt_id: The prompt ID (filename without .yaml)
            
        Returns:
            Prompt object
            
        Raises:
            FileNotFoundError: If prompt file doesn't exist
            yaml.YAMLError: If YAML is invalid
        """
        path = self._resolve_path(prompt_id)
        
        if not path.exists():
            raise FileNotFoundError(f"Prompt not found: {prompt_id}")
        
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
        
        return Prompt.from_dict(data)
    
    def _resolve_path(self, prompt_id: str) -> Path:
        """Resolve prompt ID to file path."""
        return self.prompts_dir / f"{prompt_id}.yaml"
```

### Application Layer Example

```python
"""
grompt commit command - Version and hash a prompt.
"""

import click
from pathlib import Path
from typing import Optional
from grompt.infrastructure.storage.yaml_loader import YAMLLoader
from grompt.infrastructure.storage.hasher import PromptHasher
from grompt.core.validator import PromptValidator


@click.command()
@click.argument('name')
@click.option('--force', is_flag=True, help='Force version increment')
def commit(name: str, force: bool = False) -> None:
    """
    Commit changes to a prompt (increment version only if content changed).
    
    Args:
        name: Prompt name/ID
        force: Force version increment even if unchanged
    """
    # Load config and prompt
    loader = YAMLLoader()
    prompt = loader.load_prompt(name)
    
    # Validate
    validation_result = PromptValidator.validate(prompt)
    if not validation_result.passed:
        click.echo(f"Validation failed: {validation_result.errors}")
        return
    
    # Check for changes
    new_hash = PromptHasher.generate_hash(prompt)
    if prompt.hash == new_hash and not force:
        click.echo("No changes detected.")
        return
    
    # Commit
    prompt.version += 1
    prompt.hash = new_hash
    loader.save(prompt)
    
    click.echo(f"Committed {name} (version {prompt.version})")
```

---

## Quick Reference Checklist

Before submitting code, ensure:

- [ ] Code formatted with Black (`black grompt/ tests/`)
- [ ] Linting passes (`ruff check grompt/ tests/`)
- [ ] Type checking passes (`mypy grompt/`)
- [ ] All tests pass (`pytest`)
- [ ] Type hints on all functions
- [ ] Docstrings on all public APIs
- [ ] Layer dependencies respected (Core → Infrastructure → Application)
- [ ] No I/O in Core layer
- [ ] Error handling with specific exceptions
- [ ] Descriptive variable/function names
- [ ] Tests added for new functionality

---

## IDE Configuration

### VS Code

Add to `.vscode/settings.json`:

```json
{
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true,
  "python.linting.mypyEnabled": true,
  "editor.formatOnSave": true,
  "editor.rulers": [100],
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter"
  }
}
```

### PyCharm

1. **Black**: Install Black plugin, set as formatter
2. **Ruff**: Install Ruff plugin, enable as linter
3. **MyPy**: Configure MyPy in Settings → Tools → MyPy
4. **Line Length**: Settings → Editor → Code Style → Hard wrap at 100

---

## Summary

- **Architecture**: Clean Architecture (Core → Infrastructure → Application)
- **Style**: Black (100 chars), Ruff, MyPy
- **Types**: Required on all functions
- **Docs**: Google-style docstrings
- **Tests**: pytest, high coverage
- **Dependencies**: Minimal, layer-specific
- **Naming**: `snake_case` functions, `PascalCase` classes

Follow these guidelines to maintain code quality and consistency across the Grompt codebase.

