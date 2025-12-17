# Grompt - Git for Prompts

[![PyPI version](https://img.shields.io/pypi/v/grompt.svg)](https://pypi.org/project/grompt/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-passing-green)](https://github.com/mkarots/grompt/actions)
[![Coverage](https://codecov.io/gh/mkarots/grompt/branch/main/graph/badge.svg)](https://codecov.io/gh/mkarots/grompt)
[![Python Versions](https://img.shields.io/pypi/pyversions/grompt.svg)](https://pypi.org/project/grompt/)

**Store prompts as YAML files, version them, and use them in code by ID.**

That's it. Everything else is optional.

---

## The Core Idea

**Grompt lets you store prompts as YAML files, version them, and use them in code by ID.**

- ✅ Prompts live in files (`prompts/code-review.yaml`) - not buried in code
- ✅ Version changes with `grompt commit code-review`
- ✅ Use in code: `prompt = grompt.load("code-review")`

**That's the core.** Everything else is nice-to-have.

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

## What Grompt Is

### 1. Prompt Storage
- Prompts live in YAML files (`prompts/code-review.yaml`)
- Not buried in code
- Easy to edit, review, and share

### 2. Versioning
- Track changes with version numbers
- Commit changes: `grompt commit code-review`
- Only version when content actually changes (hash-based)

### 3. Use in Code
```python
import grompt
prompt = grompt.load("code-review")
result = prompt.render(code="...", language="Python")
```

---

## What Grompt Is NOT

- ❌ **Not a test runner** - Use pytest for that
- ❌ **Not an LLM execution engine** - Just manages prompts
- ❌ **Not a prompt optimization tool** - Just stores and versions them
- ❌ **Not a database** - Just files

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

### The Simple Workflow

```
1. Create prompt file    → prompts/code-review.yaml
2. Edit it               → vim prompts/code-review.yaml
3. Test it               → Use test inputs or pytest
4. Commit changes        → grompt commit code-review
5. Use in code          → grompt.load("code-review")
```

### Step-by-Step

**1. Initialize Grompt**

Initialize Grompt in your project root. This creates a `.grompt` config file and a `prompts` directory.

```bash
grompt init
```

**2. Create a Prompt**

Create a new prompt named `code-review`.

```bash
grompt add code-review --template "Review this code:\n{{ code }}"
```

This creates `prompts/code-review.yaml`.

**3. Use in Python**

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

**4. Load Variables from Files (Optional)**

Use the optional helper to load test inputs from YAML files:

```python
import grompt

prompt = grompt.load("code-review")

# Load variables from any YAML file
variables = grompt.load_variables("inputs/simple.yaml")
result = prompt.render(**variables)
```

**5. Commit Changes**

Commit changes when you're ready:

```bash
grompt commit code-review "Updated template"
```

---

## File Structure

```
my-project/
├── prompts/
│   ├── code-review.yaml              ← Your prompts
│   └── test-inputs/                  ← Example inputs (optional)
│       └── code-review.simple.yaml
└── .grompt/                          ← Config (auto-created)
    └── config.yaml
```

**Just files.** Nothing hidden.

---

## Quick Reference

### Create Prompt
```bash
grompt add code-review
```

### Edit Prompt
```bash
vim prompts/code-review.yaml
```

### Test with Input
```bash
# Create input file (anywhere, any name)
cat > inputs/simple.yaml << EOF
code: "def add(a, b): return a + b"
language: Python
EOF

# Use in Python
python3 << EOF
import grompt

prompt = grompt.load("code-review")
inputs = grompt.load_variables("inputs/simple.yaml")  # Any path
result = prompt.render(**inputs)
print(result)
EOF
```

### Commit Changes
```bash
grompt commit code-review "Updated template"
```

### Use in Code
```python
import grompt
prompt = grompt.load("code-review")
result = prompt.render(code="...", language="Python")
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

## Contributing

We welcome contributions! Please see:

- [CONTRIBUTING.md](CONTRIBUTING.md) - Development setup and contribution guidelines
- [CODING_GUIDELINES.md](CODING_GUIDELINES.md) - Code style, architecture, and best practices
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) - Community standards and behavior expectations

---

## Security

For security concerns, please see [SECURITY.md](SECURITY.md).

**Please do not report security vulnerabilities through public GitHub issues.** Instead, email: mkarots@users.noreply.github.com

---

## License

MIT
