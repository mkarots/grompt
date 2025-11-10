# Grompt - Git for Prompts

**Keep It Stupid Simple**

---

## What is Grompt?

A simple system to organize, version, and manage LLM prompts separately from code.

**Think: "Git for Prompts"**

---

## The Problem

**Current state:**
```python
# Prompts buried in code
def analyze_code(code):
    prompt = f"""
    You are a code reviewer. Please analyze this code:
    
    {code}
    
    Provide feedback on:
    - Code quality
    - Potential bugs
    - Performance issues
    """
    return llm.complete(prompt)
```

**Problems:**
- ❌ Can't change prompt without changing code
- ❌ Can't version prompts independently
- ❌ Can't test prompts easily
- ❌ Can't track which prompt version is in production
- ❌ Can't optimize prompts without deploying code

---

## The Solution

**Prompts as files, code references them by ID:**

```yaml
# prompts/code-review.yaml
id: code-review
version: 2
model: gpt-4
template: |
  You are a code reviewer. Analyze this code:
  
  {{ code }}
  
  Provide feedback on:
  - Code quality
  - Potential bugs
  - Performance issues
```

```python
# Your code
from grompt import Prompt

def analyze_code(code):
    prompt = Prompt.load("code-review")
    return prompt.render(code=code)
```

**Benefits:**
- ✅ Change prompts without touching code
- ✅ Version prompts with git
- ✅ Test prompts independently
- ✅ Track prompt versions in production
- ✅ Optimize prompts separately

---

## File Format: YAML (Simple and Readable)

### Basic Prompt

```yaml
# prompts/summarize.yaml
id: summarize
version: 1
model: gpt-3.5-turbo
template: |
  Summarize this text in 3 sentences:
  
  {{ text }}
```

### Prompt with Metadata

```yaml
# prompts/code-review.yaml
id: code-review
version: 2
model: gpt-4
description: Reviews code for quality and bugs
author: john@example.com
created: 2024-01-15
updated: 2024-02-20

template: |
  You are a code reviewer. Analyze this code:
  
  {{ code }}
  
  Focus on:
  - Code quality
  - Potential bugs
  - Performance issues
```

### Prompt with System Message

```yaml
# prompts/chatbot.yaml
id: chatbot
version: 1
model: gpt-4

system: |
  You are a helpful assistant that answers questions concisely.

template: |
  {{ user_message }}
```

### Prompt with Variables

```yaml
# prompts/translate.yaml
id: translate
version: 1
model: gpt-3.5-turbo

variables:
  target_language:
    type: string
    required: true
    description: Language to translate to
  
  text:
    type: string
    required: true
    description: Text to translate

template: |
  Translate this text to {{ target_language }}:
  
  {{ text }}
```

---

## Directory Structure

```
your-project/
├── prompts/
│   ├── code-review.yaml
│   ├── summarize.yaml
│   ├── translate.yaml
│   └── chatbot.yaml
├── .grompt/
│   └── config.yaml
└── your_code.py
```

**Simple. Flat. Easy to navigate.**

---

## Python API (Keep It Simple)

### Loading Prompts

```python
from grompt import Prompt

# Load by ID
prompt = Prompt.load("code-review")

# Render with variables
text = prompt.render(code="def hello(): print('hi')")

# Get metadata
print(prompt.id)        # "code-review"
print(prompt.version)   # 2
print(prompt.model)     # "gpt-4"
```

### Using with LLM APIs

```python
from grompt import Prompt
import openai

# Load prompt
prompt = Prompt.load("code-review")

# Render
message = prompt.render(code=my_code)

# Use with OpenAI
response = openai.ChatCompletion.create(
    model=prompt.model,
    messages=[{"role": "user", "content": message}]
)
```

### Versioning

```python
# Load specific version
prompt_v1 = Prompt.load("code-review", version=1)
prompt_v2 = Prompt.load("code-review", version=2)

# Compare
print(f"v1 tokens: {prompt_v1.count_tokens(code=my_code)}")
print(f"v2 tokens: {prompt_v2.count_tokens(code=my_code)}")
```

---

## CLI Tools (Git-Style Commands)

### Core Commands (Git-like)

```bash
# Initialize a new grompt repository
$ grompt init
Initialized grompt repository in /path/to/project

# Add a prompt to staging
$ grompt add code-review
Added prompts/code-review.yaml

# Add all changed prompts
$ grompt add .

# Commit changes
$ grompt commit -m "Optimize code-review prompt"
[main abc123] Optimize code-review prompt
 1 file changed, 5 insertions(+), 8 deletions(-)

# Push to remote (syncs with git)
$ grompt push
Pushing prompts to origin/main...
Done!

# Pull from remote
$ grompt pull
Pulling prompts from origin/main...
Done!

# Show status
$ grompt status
Modified:
  prompts/code-review.yaml (v2 -> v3)
  
Untracked:
  prompts/new-prompt.yaml

# Show diff
$ grompt diff code-review
- version: 2
+ version: 3
- Review this code:
+ Review:
  {{ code }}

# Show log
$ grompt log code-review
commit abc123 - 2024-02-20
  Optimize code-review prompt (v2 -> v3)
  -12 tokens, -$0.00036/call

commit def456 - 2024-02-15
  Add code-review prompt (v1 -> v2)
  Initial version
```

### Prompt Management Commands

```bash
# List all prompts
$ grompt list
code-review (v2) - Reviews code for quality
summarize (v1) - Summarizes text
translate (v1) - Translates text
chatbot (v1) - Helpful assistant

# Show prompt details
$ grompt show code-review
ID: code-review
Version: 2
Model: gpt-4
Author: john@example.com
Updated: 2024-02-20

Template:
You are a code reviewer. Analyze this code:

{{ code }}

Focus on:
- Code quality
- Potential bugs
- Performance issues

# Test prompt
$ grompt test code-review --var code="def hello(): print('hi')"
Rendered:
You are a code reviewer. Analyze this code:

def hello(): print('hi')

Focus on:
- Code quality
- Potential bugs
- Performance issues

Tokens: 45
Cost: $0.00135 (gpt-4)

# Count tokens
$ grompt count code-review --var code="$(cat myfile.py)"
Tokens: 234
Model: gpt-4
Cost: $0.00702

# Validate all prompts
$ grompt validate
✓ code-review.yaml - valid
✓ summarize.yaml - valid
✗ translate.yaml - missing required variable: target_language
```

### Branching and Experimentation

```bash
# Create a new branch for experiments
$ grompt branch optimize-prompts
Switched to branch 'optimize-prompts'

# List branches
$ grompt branch
  main
* optimize-prompts

# Switch branches
$ grompt checkout main
Switched to branch 'main'

# Merge branches
$ grompt merge optimize-prompts
Merging optimize-prompts into main...
Done!
```

---

## Versioning Strategy

### Version in File (Simple)

```yaml
# prompts/code-review.yaml
id: code-review
version: 2
template: |
  ...
```

**Use git for history:**

```bash
# See prompt changes
$ git log prompts/code-review.yaml

# See what changed
$ git diff prompts/code-review.yaml

# Revert to old version
$ git checkout HEAD~1 prompts/code-review.yaml
```

---

## Git Integration

### Track Changes

```bash
# See prompt changes
$ git log prompts/code-review.yaml

# See what changed
$ git diff prompts/code-review.yaml

# Revert to old version
$ git checkout HEAD~1 prompts/code-review.yaml
```

### Branching for Experiments

```bash
# Create branch for prompt experiments
$ git checkout -b optimize-code-review

# Edit prompt
$ vim prompts/code-review.yaml

# Test
$ grompt test code-review

# Merge if better
$ git checkout main
$ git merge optimize-code-review
```

---

## Testing Prompts

### Test File Format

```yaml
# tests/code-review.test.yaml
prompt: code-review

test_cases:
  - name: Simple function
    variables:
      code: |
        def add(a, b):
            return a + b
    
    expect:
      max_tokens: 100
      contains:
        - "function"
        - "simple"
  
  - name: Complex class
    variables:
      code: |
        class Calculator:
            def add(self, a, b):
                return a + b
    
    expect:
      max_tokens: 150
```

### Run Tests

```bash
$ grompt test-run code-review
Running tests for code-review...
✓ Simple function (45 tokens)
✓ Complex class (89 tokens)

All tests passed!
```

---

## Configuration

```yaml
# .grompt/config.yaml
prompts_dir: prompts
default_model: gpt-4

models:
  gpt-4:
    max_tokens: 8192
    pricing:
      input: 0.03
      output: 0.06
  
  gpt-3.5-turbo:
    max_tokens: 4096
    pricing:
      input: 0.0005
      output: 0.0015
```

---

## Architecture: Core-Application-Infrastructure

### Directory Structure

```
grompt/
├── core/                    # Core domain logic (pure, no dependencies)
│   ├── __init__.py
│   ├── prompt.py           # Prompt entity
│   ├── template.py         # Template rendering
│   └── tokenizer.py        # Token counting logic
│
├── application/             # Application layer (use cases, CLI)
│   ├── __init__.py
│   ├── cli/
│   │   ├── __init__.py
│   │   ├── main.py         # CLI entry point
│   │   └── commands/
│   │       ├── init.py
│   │       ├── add.py
│   │       ├── commit.py
│   │       ├── test.py
│   │       └── count.py
│   │
│   └── use_cases/
│       ├── load_prompt.py
│       ├── render_prompt.py
│       └── count_tokens.py
│
├── infrastructure/          # External integrations & adapters
│   ├── __init__.py
│   ├── storage/
│   │   ├── yaml_loader.py  # YAML file loader
│   │   └── git_adapter.py  # Git operations
│   │
│   ├── llm/
│   │   ├── openai.py       # OpenAI integration
│   │   ├── anthropic.py    # Anthropic integration
│   │   └── base.py         # Base LLM interface
│   │
│   └── testing/
│       ├── runner.py       # Test runner
│       └── validator.py    # Prompt validator
│
├── prompts/                 # Your prompts (user data)
│   ├── code-review.yaml
│   ├── summarize.yaml
│   └── translate.yaml
│
├── tests/                   # Prompt tests
│   ├── code-review.test.yaml
│   └── summarize.test.yaml
│
├── .grompt/
│   └── config.yaml
│
├── pyproject.toml
└── README.md
```

### Layer Responsibilities

#### Core Layer (Pure Domain Logic)
- **No external dependencies**
- Contains business logic only
- Prompt entity and operations
- Template rendering logic
- Token counting algorithms

```python
# core/prompt.py
from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class Prompt:
    """Core Prompt entity - pure domain model"""
    id: str
    version: int
    model: str
    template: str
    system: Optional[str] = None
    variables: Dict = None
    metadata: Dict = None
    
    def __post_init__(self):
        if self.variables is None:
            self.variables = {}
        if self.metadata is None:
            self.metadata = {}
```

```python
# core/template.py
from jinja2 import Template

class TemplateRenderer:
    """Pure template rendering logic"""
    
    @staticmethod
    def render(template: str, **kwargs) -> str:
        """Render a Jinja2 template with variables"""
        t = Template(template)
        return t.render(**kwargs)
```

```python
# core/tokenizer.py
import tiktoken

class TokenCounter:
    """Pure token counting logic"""
    
    @staticmethod
    def count(text: str, model: str = "gpt-4") -> int:
        """Count tokens for a given model"""
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))
```

#### Application Layer (Use Cases & CLI)
- **Orchestrates core logic**
- CLI commands
- Use case implementations
- Business workflows

```python
# application/use_cases/load_prompt.py
from core.prompt import Prompt
from infrastructure.storage.yaml_loader import YAMLLoader

class LoadPromptUseCase:
    """Use case: Load a prompt by ID"""
    
    def __init__(self, loader: YAMLLoader):
        self.loader = loader
    
    def execute(self, prompt_id: str) -> Prompt:
        """Load and return a prompt"""
        data = self.loader.load(prompt_id)
        return Prompt(
            id=data['id'],
            version=data['version'],
            model=data.get('model', 'gpt-4'),
            template=data['template'],
            system=data.get('system'),
            variables=data.get('variables', {}),
            metadata={k: v for k, v in data.items()
                     if k not in ['id', 'version', 'model', 'template', 'system', 'variables']}
        )
```

```python
# application/cli/commands/test.py
import click
from application.use_cases.load_prompt import LoadPromptUseCase
from core.template import TemplateRenderer
from core.tokenizer import TokenCounter
from infrastructure.storage.yaml_loader import YAMLLoader

@click.command()
@click.argument('prompt_id')
@click.option('--var', multiple=True)
def test(prompt_id: str, var: tuple):
    """Test a prompt with variables"""
    # Parse variables
    variables = {}
    for v in var:
        key, value = v.split('=', 1)
        variables[key] = value
    
    # Load prompt (use case)
    loader = YAMLLoader()
    use_case = LoadPromptUseCase(loader)
    prompt = use_case.execute(prompt_id)
    
    # Render (core logic)
    rendered = TemplateRenderer.render(prompt.template, **variables)
    
    # Count tokens (core logic)
    tokens = TokenCounter.count(rendered, prompt.model)
    
    # Display
    click.echo("Rendered:")
    click.echo(rendered)
    click.echo(f"\nTokens: {tokens}")
    click.echo(f"Model: {prompt.model}")
```

#### Infrastructure Layer (External Integrations)
- **Adapters for external systems**
- File I/O (YAML loading)
- Git operations
- LLM API integrations
- Testing framework

```python
# infrastructure/storage/yaml_loader.py
from pathlib import Path
import yaml

class YAMLLoader:
    """Adapter for loading YAML files"""
    
    def __init__(self, prompts_dir: Path = Path("prompts")):
        self.prompts_dir = prompts_dir
    
    def load(self, prompt_id: str) -> dict:
        """Load a prompt YAML file"""
        path = self.prompts_dir / f"{prompt_id}.yaml"
        with open(path) as f:
            return yaml.safe_load(f)
```

```python
# infrastructure/llm/openai.py
import openai
from core.prompt import Prompt
from core.template import TemplateRenderer

class OpenAIAdapter:
    """Adapter for OpenAI API"""
    
    def complete(self, prompt: Prompt, **kwargs) -> str:
        """Complete a prompt using OpenAI"""
        message = TemplateRenderer.render(prompt.template, **kwargs)
        
        response = openai.ChatCompletion.create(
            model=prompt.model,
            messages=[{"role": "user", "content": message}]
        )
        
        return response.choices[0].message.content
```

```python
# infrastructure/storage/git_adapter.py
import subprocess
from pathlib import Path

class GitAdapter:
    """Adapter for Git operations"""
    
    def __init__(self, repo_path: Path = Path(".")):
        self.repo_path = repo_path
    
    def add(self, file_path: str):
        """Git add a file"""
        subprocess.run(["git", "add", file_path], cwd=self.repo_path)
    
    def commit(self, message: str):
        """Git commit"""
        subprocess.run(["git", "commit", "-m", message], cwd=self.repo_path)
    
    def push(self):
        """Git push"""
        subprocess.run(["git", "push"], cwd=self.repo_path)
```

---

## Example Workflows

### Workflow 1: Creating Your First Prompt

```bash
# Initialize grompt
$ grompt init
Initialized grompt repository
Created prompts/ directory
Created .grompt/config.yaml

# Create a prompt
$ cat > prompts/code-review.yaml << EOF
id: code-review
version: 1
model: gpt-4
template: |
  Review this code:
  {{ code }}
EOF

# Test it
$ grompt test code-review --var code="def hello(): pass"
Rendered:
Review this code:
def hello(): pass

Tokens: 12
Cost: $0.00036

# Add and commit
$ grompt add code-review
$ grompt commit -m "Add code-review prompt"
$ grompt push
```

### Workflow 2: Using in Your Application

```python
# your_app.py
from application.use_cases.load_prompt import LoadPromptUseCase
from infrastructure.storage.yaml_loader import YAMLLoader
from infrastructure.llm.openai import OpenAIAdapter

def review_code(code: str) -> str:
    # Load prompt
    loader = YAMLLoader()
    use_case = LoadPromptUseCase(loader)
    prompt = use_case.execute("code-review")
    
    # Use with OpenAI
    adapter = OpenAIAdapter()
    return adapter.complete(prompt, code=code)
```

---

## Why This Works

1. **Simple** - Just YAML files
2. **Git-friendly** - Text files, easy to diff
3. **Testable** - Separate prompts from code
4. **Versionable** - Track changes over time
5. **Portable** - Works with any LLM API
6. **Toolable** - Easy to build tools around

---

## Getting Started

```bash
# Install
pip install grompt

# Initialize
grompt init

# Create first prompt
cat > prompts/hello.yaml << EOF
id: hello
version: 1
model: gpt-3.5-turbo
template: |
  Say hello to {{ name }}
EOF

# Test it
grompt test hello --var name="World"

# Use it
python -c "
from grompt import Prompt
p = Prompt.load('hello')
print(p.render(name='World'))
"
```

**That's it. Keep it simple.**

---

## Implementation Phases

### Phase 1: Core (MVP)
- YAML parser
- Prompt class (load, render)
- CLI: `list`, `show`, `test`
- Token counting (tiktoken)

### Phase 2: Testing
- Test file format
- Test runner
- Validation

### Phase 3: Optimization
- Cost tracking
- Version comparison
- Analytics

---

## Name Origin

**Grompt** = **Gr**it + Pr**ompt**

Because prompts should be version controlled like code.