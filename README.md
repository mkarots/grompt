# Grompt - Git for Prompts

[![PyPI version](https://img.shields.io/pypi/v/grompt.svg)](https://pypi.org/project/grompt/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-passing-green)](https://github.com/yourusername/grompt/actions)
[![Coverage](https://codecov.io/gh/yourusername/grompt/branch/main/graph/badge.svg)](https://codecov.io/gh/yourusername/grompt)
[![Python Versions](https://img.shields.io/pypi/pyversions/grompt.svg)](https://pypi.org/project/grompt/)

**Version, test, and manage LLM prompts separately from code.**

Grompt lets you store prompts as YAML files, version them with git, test them with real data, and use them in your code by ID. Change prompts without deploying code.

---

## Why Grompt?

**Problem:** Prompts buried in code are hard to version, test, and optimize.
**Solution:** Prompts as files, referenced by ID.

**Benefits:**
- ✅ Change prompts without touching code
- ✅ Version prompts with git
- ✅ Test prompts with real data
- ✅ Track which version is in production

---

## Installation

Install Grompt via pip:

```bash
pip install grompt
```

For development installation:

```bash
pip install -e ".[dev]"
```

---

## Quick Start

### 1. Initialize Grompt

Initialize Grompt in your project root. This creates a `.grompt` config file and a `prompts` directory.

```bash
grompt init
```

### 2. Create a Prompt

Create a new prompt named `code-review`.

```bash
grompt add code-review --template "Review this code:\n{{ code }}"
```

This creates `prompts/code-review.yaml`.

### 3. Test it with Data

Run the prompt with sample data to verify the output.

```bash
grompt test code-review --var code="def hello(): pass"
```

### 4. Use in Python

Load and use the prompt in your application.

```python
import grompt

# Load the prompt
prompt = grompt.load("code-review")

# Render with variables
rendered = prompt.render(
    code="def add(a,b): return a+b"
)
print(rendered)
```

---

## Documentation

- [Defining Prompts](docs/defining_prompts.md) - Learn how to create prompts with variables, system messages, and more.
- [Using Prompts](docs/using_prompts.md) - How to use prompts in your CLI and Python code.
- [Testing Prompts](docs/testing.md) - Creating test cases and running tests.
- [Variable Validation](docs/validation.md) - Ensuring inputs match expected schemas.
- [CLI Reference](docs/cli.md) - Complete command-line interface documentation.
- [Python API](docs/api.md) - API reference for integrating Grompt.
- [Configuration](docs/configuration.md) - Global configuration options.
- [Best Practices](docs/best_practices.md) - Tips for managing prompts effectively.
- [Examples](docs/examples.md) - Real-world usage examples.

---

## License

MIT
