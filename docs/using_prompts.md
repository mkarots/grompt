# Using Prompts with Variables

## Python API

```python
import grompt

# Load prompt
prompt = grompt.load("code-review")

# Simple rendering
rendered = prompt.render(
    code="def add(a, b): return a + b"
)

# Multiple variables
rendered = prompt.render(
    code="def add(a, b): return a + b",
    language="Python",
    focus_areas=["quality", "type hints"]
)

# Load variables from YAML file (optional helper)
variables = grompt.load_variables("inputs/simple.yaml")
rendered = prompt.render(**variables)

# Or load from any file path
variables = grompt.load_variables("test-inputs/code-review.example1.yaml")
rendered = prompt.render(**variables)

# With system message
if prompt.system:
    system_msg = prompt.system
    user_msg = rendered
    # Use both with your LLM API
```

## Loading Variables from Files

The `load_variables()` helper lets you organize test inputs however you want:

```python
import grompt

# Load prompt
prompt = grompt.load("code-review")

# Load variables from any YAML file
variables = grompt.load_variables("prompts/test-inputs/code-review.simple.yaml")
rendered = prompt.render(**variables)

# Or use your own structure
variables = grompt.load_variables("data/inputs/example1.yaml")
rendered = prompt.render(**variables)
```

**No enforced structure** - organize files however makes sense for your project.

## Using with LLM APIs

```python
import grompt
import openai

# Load and render
prompt = grompt.load("code-review")
message = prompt.render(
    code=my_code,
    language="Python"
)

# Use with OpenAI
response = openai.ChatCompletion.create(
    model=prompt.model,
    messages=[
        {"role": "system", "content": prompt.system} if prompt.system else None,
        {"role": "user", "content": message}
    ]
)
```

