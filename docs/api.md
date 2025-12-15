# Python API Reference

## Loading Prompts

```python
from grompt.infrastructure.storage.yaml_loader import YAMLLoader

loader = YAMLLoader()

# Load by ID
prompt = loader.load_prompt("code-review")

# Access properties
print(prompt.id)          # "code-review"
print(prompt.version)     # 2
print(prompt.model)       # "gpt-4"
print(prompt.template)    # Template string
print(prompt.variables)   # Variable definitions
```

## Rendering Templates

```python
from grompt import TemplateRenderer

# Simple rendering
rendered = TemplateRenderer.render(
    "Hello {{ name }}!",
    name="World"
)

# With prompt
rendered = TemplateRenderer.render(
    prompt.template,
    code="def add(a, b): return a + b",
    language="Python"
)

# Validate template
is_valid = TemplateRenderer.validate(prompt.template)
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

# Validate variable types
def validate_vars(user_input):
    for name, spec in prompt.variables.items():
        if spec.get('required') and name not in user_input:
            raise ValueError(f"Missing required variable: {name}")
```

