# Code Review Assistant Example

This example demonstrates how to use Grompt in a real Python application with OpenAI integration.

## Quick Start

```bash
# 1. Install Grompt and OpenAI
pip install grompt openai

# 2. Set your OpenAI API key
export OPENAI_API_KEY=your_api_key_here

# 3. Setup the example
python setup.py

# 4. Run the enhanced example (with OpenAI)
python app_enhanced.py
```

## What This Demonstrates

✅ **Prompts stored separately**: The prompt is in `prompts/code-review.yaml`, not hardcoded in the app  
✅ **Easy to change**: Modify `prompts/code-review.yaml` without touching `app.py`  
✅ **Version control**: The prompt is versioned with git  
✅ **Clean API**: Simple `grompt.load()` and `prompt.render()` calls  
✅ **No code deploys needed**: Change prompts without deploying code  
✅ **Few-shot examples**: Pass examples as a list to improve LLM responses  
✅ **Real LLM integration**: Uses OpenAI API with model from prompt parameters

## Example Usage

```python
import grompt
import os
from openai import OpenAI

# Load prompt (stored in prompts/code-review.yaml)
prompt = grompt.load("code-review")

# Define few-shot examples
examples = [
    "Code: def safe_divide(x, y): ...\nReview: Good error handling...",
    "Code: def get_user(id): ...\nReview: Excellent use of parameterized queries..."
]

# Render with variables including examples
rendered = prompt.render(
    code="def add(a, b): return a + b",
    language="Python",
    examples=examples
)

# Use with OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
response = client.chat.completions.create(
    model=prompt.parameters.get("model", "gpt-4"),
    messages=[{"role": "user", "content": rendered}]
)
```

## Features

### Few-Shot Examples

The prompt template supports few-shot examples passed as a list:

```python
examples = [
    "Example 1: Code review format...",
    "Example 2: Another example..."
]

result = reviewer.review(
    code="def divide(x, y): return x / y",
    language="Python",
    examples=examples
)
```

The template uses Jinja2 to format the examples:

```yaml
{% if examples %}
Here are some examples of good code reviews:

{% for example in examples %}
Example {{ loop.index }}:
{{ example }}

{% endfor %}
{% endif %}
```

### OpenAI Integration

- Uses model from `prompt.parameters.model` (defaults to "gpt-4")
- Supports temperature and max_tokens from parameters
- Handles system messages if present in prompt
- Graceful fallback if API key not set

## Try It Out

1. **Set your API key**:
   ```bash
   export OPENAI_API_KEY=your_key_here
   ```

2. **Run the app**:
   ```bash
   python app_enhanced.py
   ```

3. **Modify the prompt** without changing code:
   ```bash
   # Edit prompts/code-review.yaml
   # Or use CLI:
   grompt add code-review --template "Your new template"
   ```

4. **Run again** - same code, different prompt!

## Files

- `app.py` - Basic example showing prompt loading and rendering
- `app_enhanced.py` - Enhanced example with OpenAI integration and few-shot examples
- `setup.py` - Automated setup script
- `prompts/code-review.yaml` - The prompt file (versioned separately)

## Configuration

The prompt parameters in `prompts/code-review.yaml` control the OpenAI API:

```yaml
parameters:
  model: gpt-4          # Model to use
  temperature: 0.7      # Sampling temperature
  max_tokens: 1000      # Maximum tokens in response
```

## Error Handling

The app gracefully handles:
- Missing OpenAI library (shows install instructions)
- Missing API key (uses fallback mode)
- API errors (shows error message)

## Next Steps

In a production app, you would:

1. **Use the executor system**:
   ```python
   from grompt.core.execution import register_executor
   
   class OpenAIExecutor:
       def execute(self, prompt, inputs):
           rendered = prompt.render(**inputs)
           # Call OpenAI...
   
   register_executor("openai", OpenAIExecutor())
   ```

2. **Add test cases** for your prompts:
   ```yaml
   test_cases:
     - name: "division_bug"
       input:
         code: "def divide(x, y): return x / y"
       expected_meaning:
         - "warns about division by zero"
   ```

3. **Version prompts** with git:
   ```bash
   grompt commit code-review "Added few-shot examples"
   ```
