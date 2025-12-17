# Example Apps

This directory contains example applications demonstrating Grompt usage.

## Code Review Assistant

A simple code review tool that uses Grompt-managed prompts.

**Location:** `code-review-app/`

**Features:**
- Loads prompts from YAML files
- Renders prompts with Jinja2 templating
- Simulates LLM API integration
- Shows how to change prompts without code changes

**Run it:**
```bash
cd code-review-app
python setup.py
python app_enhanced.py
```

See `code-review-app/README.md` for details.

