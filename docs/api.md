# Python API Reference

## Loading Prompts

```python
import grompt

# Load by ID (defaults to reading from 'prompts' directory)
prompt = grompt.load("code-review")

# Load by absolute file path
prompt = grompt.load("/path/to/my-prompt.yaml")

# Load from a specific directory or use a specific loader
prompt = grompt.load("code-review", prompts_dir="my_prompts", loader="yaml")

# Access properties
print(prompt.id)          # "code-review"
print(prompt.version)     # 2
print(prompt.model)       # "gpt-4"
print(prompt.template)    # Template string
print(prompt.variables)   # Variable definitions
```

## Rendering Prompts

```python
# Render directly from the prompt object
rendered = prompt.render(
    code="def add(a, b): return a + b",
    language="Python"
)

print(rendered)
```

## Advanced: Using Lower-Level Classes

If you need more control, you can still access the underlying classes:

```python
from grompt.infrastructure.storage.yaml_loader import YAMLLoader
from grompt import TemplateRenderer

loader = YAMLLoader()
prompt = loader.load_prompt("code-review")

rendered = TemplateRenderer.render(
    prompt.template,
    code="def add(a, b): return a + b"
)
```

## Working with Variables

```python
# Get required variables
required_vars = [
    name for name, spec in prompt.variables.items()
    if spec.get('required', False)
]

# Get variable with default
def get_var_value(var_name, user_input):
    spec = prompt.variables.get(var_name, {})
    return user_input.get(var_name, spec.get('default'))
```
