# Grompt CLI Commands - Simplified

## Core Commands

### `grompt init`

**Purpose**: Initialize a grompt project in the current directory

**What it does**:
- Creates `.grompt` file (or `.grompt/config.yaml`)
- Creates `prompts/` directory if it doesn't exist
- Sets up basic configuration

**Usage**:
```bash
$ grompt init
Initialized grompt project
Created .grompt
Created prompts/ directory
```

**`.grompt` file format**:
```yaml
version: 1
prompts_dir: prompts
default_model: gpt-4
```

---

### `grompt add <name> [options]`

**Purpose**: Create a new prompt file

**What it does**:
- Creates a new YAML file in the prompts directory
- Optionally populates it with CLI arguments
- If no options given, creates a minimal template

**Usage**:

**Basic (creates empty template)**:
```bash
$ grompt add code-review
Created prompts/code-review.yaml
```

**With options (populates the file)**:
```bash
$ grompt add code-review \
  --model gpt-4 \
  --template "Review this code: {{ code }}" \
  --description "Reviews code for quality"

Created prompts/code-review.yaml
```

**With directory**:
```bash
$ grompt add backend/code-review --model gpt-4
Created prompts/backend/code-review.yaml
```

**Generated file (minimal)**:
```yaml
id: code-review
version: 1
model: gpt-4
template: |
  # Add your prompt template here
  # Use {{ variable_name }} for variables
```

**Generated file (with options)**:
```yaml
id: code-review
version: 1
model: gpt-4
description: Reviews code for quality
template: |
  Review this code: {{ code }}
```

**CLI Options**:
- `--model <model>`: Set the model (default: gpt-4)
- `--template <text>`: Set the template text
- `--description <text>`: Add a description
- `--system <text>`: Add a system message
- `--dir <path>`: Create in subdirectory

---

### `grompt commit <name> [message]`

**Purpose**: Commit changes to a prompt (increment version and hash it)

**What it does**:
1. Reads the current prompt file
2. Increments the version number
3. Generates a hash of the prompt content
4. Saves the updated file
5. Optionally records the change in a history file

**Usage**:

**Basic commit**:
```bash
$ grompt commit code-review
Committed code-review
  version: 1 -> 2
  hash: abc123def456
```

**With message**:
```bash
$ grompt commit code-review "Optimized for fewer tokens"
Committed code-review
  version: 1 -> 2
  hash: abc123def456
  message: Optimized for fewer tokens
```

**What happens to the file**:

**Before**:
```yaml
id: code-review
version: 1
model: gpt-4
template: |
  Review this code: {{ code }}
```

**After**:
```yaml
id: code-review
version: 2
hash: abc123def456
model: gpt-4
template: |
  Review this code: {{ code }}
```

**History tracking** (optional `.grompt/history.yaml`):
```yaml
code-review:
  - version: 1
    hash: xyz789abc123
    timestamp: 2024-02-20T10:00:00Z
    message: Initial version
  
  - version: 2
    hash: abc123def456
    timestamp: 2024-02-20T15:30:00Z
    message: Optimized for fewer tokens
```

---

### `grompt test <name>` (Future)

**Purpose**: Run tests against a prompt

**What it does** (to be defined):
- Load test cases for the prompt
- Render the prompt with test variables
- Validate output meets expectations
- Report results

**Possible usage**:
```bash
$ grompt test code-review
Running tests for code-review...
✓ Test case 1: Simple function
✓ Test case 2: Complex class
✗ Test case 3: Edge case
  Expected max 100 tokens, got 150

2/3 tests passed
```

**Test file format** (to be defined):
```yaml
# tests/code-review.test.yaml
prompt: code-review

test_cases:
  - name: Simple function
    variables:
      code: "def add(a, b): return a + b"
    expect:
      max_tokens: 100
  
  - name: Complex class
    variables:
      code: "class Calculator:\n  def add(self, a, b):\n    return a + b"
    expect:
      max_tokens: 150
```

---

## Command Summary

| Command | Purpose | Example |
|---------|---------|---------|
| `grompt init` | Initialize project | `grompt init` |
| `grompt add <name>` | Create new prompt | `grompt add code-review --model gpt-4` |
| `grompt commit <name>` | Version and hash prompt | `grompt commit code-review "Optimized"` |
| `grompt test <name>` | Run tests (future) | `grompt test code-review` |

---

## Workflow Example

```bash
# 1. Initialize project
$ grompt init
Initialized grompt project

# 2. Create a new prompt
$ grompt add code-review \
  --model gpt-4 \
  --template "Review this code: {{ code }}"
Created prompts/code-review.yaml

# 3. Edit the prompt manually
$ vim prompts/code-review.yaml
# Make changes...

# 4. Commit the changes
$ grompt commit code-review "Optimized for fewer tokens"
Committed code-review
  version: 1 -> 2
  hash: abc123def456

# 5. Use in your code
$ python
>>> from grompt import Prompt
>>> p = Prompt.load("code-review")
>>> print(p.version)  # 2
>>> print(p.hash)     # abc123def456
```

---

## Hash Generation

**Purpose**: Create a unique identifier for each prompt version

**Algorithm**:
```python
import hashlib
import yaml

def generate_hash(prompt_data: dict) -> str:
    """Generate a hash of the prompt content"""
    # Only hash the content that matters
    content = {
        'id': prompt_data['id'],
        'model': prompt_data['model'],
        'template': prompt_data['template'],
        'system': prompt_data.get('system'),
    }
    
    # Create deterministic YAML string
    yaml_str = yaml.dump(content, sort_keys=True)
    
    # Generate SHA256 hash
    hash_obj = hashlib.sha256(yaml_str.encode())
    
    # Return first 12 characters (like git)
    return hash_obj.hexdigest()[:12]
```

**Example**:
```python
>>> generate_hash({
...     'id': 'code-review',
...     'model': 'gpt-4',
...     'template': 'Review this code: {{ code }}'
... })
'abc123def456'
```

---

## File Structure After Commands

```
your-project/
├── .grompt                  # Created by: grompt init
├── prompts/                 # Created by: grompt init
│   ├── code-review.yaml    # Created by: grompt add code-review
│   └── summarize.yaml      # Created by: grompt add summarize
└── tests/                   # Created manually or by future command
    └── code-review.test.yaml
```

---

## Implementation Notes

### `grompt init`
- Check if `.grompt` already exists (don't overwrite)
- Create `prompts/` directory
- Write minimal config

### `grompt add`
- Parse CLI arguments
- Generate YAML file
- Create subdirectories if needed
- Validate prompt ID (no spaces, lowercase, etc.)

### `grompt commit`
- Read current file
- Increment version
- Generate hash
- Write updated file
- Optionally update history

### `grompt test`
- To be designed based on testing needs
- Should support multiple test cases
- Should validate token counts, output format, etc.