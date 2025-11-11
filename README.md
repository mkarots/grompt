# Grompt - Git for Prompts

A simple system to organize, version, and manage LLM prompts separately from code.

## Installation

```bash
pip install -e .
```

## Quick Start

```bash
# Initialize a grompt project
grompt init

# Create a new prompt
grompt add my-prompt --template "Summarize: {{ text }}"

# Edit the prompt
vim prompts/my-prompt.yaml

# Commit changes (increments version and generates hash)
grompt commit my-prompt "Initial version"
```

## Usage

### Initialize Project

```bash
grompt init
```

Creates:
- `.grompt` config file
- `prompts/` directory

### Create Prompts

```bash
# Basic prompt
grompt add code-review

# With options
grompt add code-review \
  --model gpt-4 \
  --template "Review this code: {{ code }}" \
  --description "Reviews code for quality"

# In subdirectory
grompt add backend/api-prompt --dir backend
```

### Commit Changes

```bash
# Basic commit
grompt commit code-review

# With message
grompt commit code-review "Optimized for fewer tokens"
```

This will:
1. Increment the version number
2. Generate a hash of the prompt content
3. Update the YAML file

### Use in Python

```python
from grompt import Prompt
from grompt.infrastructure.storage.yaml_loader import YAMLLoader

# Load a prompt
loader = YAMLLoader()
prompt = loader.load_prompt("code-review")

# Render with variables
from grompt.core.template import TemplateRenderer
rendered = TemplateRenderer.render(prompt.template, code="def hello(): pass")

print(f"Version: {prompt.version}")
print(f"Hash: {prompt.hash}")
print(f"Rendered: {rendered}")
```

## Prompt File Format

```yaml
id: code-review
version: 2
hash: abc123def456
model: gpt-4
description: Reviews code for quality
template: |
  Review this code:
  {{ code }}
```

## Architecture

Grompt follows the **Core-Application-Infrastructure** pattern:

- **Core**: Pure domain logic (Prompt entity, TemplateRenderer)
- **Application**: CLI commands and use cases
- **Infrastructure**: External adapters (YAML loader, hash generation)

## Development

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black grompt/

# Type check
mypy grompt/
```

## Optional Add-ons

### Token Counting

Install with token counting support:

```bash
pip install -e ".[tokenizer]"
```

Then use:

```python
from grompt.core.tokenizer import TokenCounter

tokens = TokenCounter.count("Your text here", model="gpt-4")
print(f"Tokens: {tokens}")
```

## License

MIT