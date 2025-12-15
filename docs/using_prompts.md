# Using Prompts with Variables

## CLI Testing

```bash
# Single variable
grompt test summarize --var text="Long article here..."

# Multiple variables
grompt test translate \
  --var target_language="Spanish" \
  --var text="Hello, world!"

# Variables from file
grompt test code-review --var code="$(cat myfile.py)"

# Complex variables (JSON)
grompt test advanced --var items='[{"name":"x","value":1}]'
```

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

# With system message
if prompt.system:
    system_msg = prompt.system
    user_msg = rendered
    # Use both with your LLM API
```

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

