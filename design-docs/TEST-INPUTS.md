# Test Inputs: File-Based Input Management

## The Need

**Problem**: Need to test prompts with well-known inputs, track performance, and experiment with different input combinations (e.g., few-shot examples).

**Solution**: Store test inputs as files, reference them by name, use them for testing and validation.

---

## Core Concept

**It's just files. That's it.**

```
prompts/
├── code-review.yaml                    ← Prompt
├── test-inputs/                        ← Test inputs folder
│   ├── code-review.simple.yaml         ← Simple input
│   ├── code-review.examples-1.yaml     ← 1 example
│   ├── code-review.examples-3.yaml     ← 3 examples
│   └── code-review.complex.yaml        ← Complex input
```

**Each input file is a YAML file with variables.**

---

## File Structure

### Option 1: Flat Structure (Recommended)

```
prompts/
├── code-review.yaml
└── test-inputs/
    ├── code-review.simple.yaml
    ├── code-review.examples-1.yaml
    ├── code-review.examples-3.yaml
    └── code-review.complex.yaml
```

**Pros**:
- Simple: All inputs in one folder
- Easy to glob: `test-inputs/code-review.*.yaml`
- Clear naming: `{prompt-id}.{input-name}.yaml`

### Option 2: Nested Structure

```
prompts/
├── code-review.yaml
└── test-inputs/
    └── code-review/
        ├── simple.yaml
        ├── examples-1.yaml
        ├── examples-3.yaml
        └── complex.yaml
```

**Pros**:
- Organized: Grouped by prompt
- Cleaner: Shorter filenames

**Cons**:
- More complex: Need subdirectories
- Harder to glob: Need recursive search

**Recommendation**: Option 1 (flat structure) - simpler, aligns with "just files" philosophy.

---

## Input File Format

### Basic Input File

```yaml
# prompts/test-inputs/code-review.simple.yaml
code: |
  def add(a, b):
      return a + b
language: Python
```

### Input with Few-Shot Examples

```yaml
# prompts/test-inputs/code-review.examples-1.yaml
code: |
  def divide(x, y):
      return x / y
language: Python
examples:
  - |
    Example 1: Good error handling
    ```python
    def safe_divide(x, y):
        if y == 0:
            raise ValueError("Cannot divide by zero")
        return x / y
    ```
```

### Input with Multiple Examples

```yaml
# prompts/test-inputs/code-review.examples-3.yaml
code: |
  def divide(x, y):
      return x / y
language: Python
examples:
  - |
    Example 1: Good error handling
    ```python
    def safe_divide(x, y):
        if y == 0:
            raise ValueError("Cannot divide by zero")
        return x / y
    ```
  - |
    Example 2: Type hints
    ```python
    def divide(x: float, y: float) -> float:
        return x / y
    ```
  - |
    Example 3: Documentation
    """Divide two numbers."""
```

### Input with Metadata (Optional)

```yaml
# prompts/test-inputs/code-review.complex.yaml
# Optional metadata
description: Complex code with multiple functions
tags: [complex, multiple-functions, classes]

# Variables
code: |
  class Calculator:
      def add(self, a, b):
          return a + b
      
      def divide(self, x, y):
          return x / y
language: Python
examples:
  - "Example with classes"
```

---

## Usage Patterns

### 1. Load Input Programmatically

```python
import grompt

# Load prompt
prompt = grompt.load("code-review")

# Load input
inputs = grompt.load_input("code-review", "simple")
# Returns: {"code": "...", "language": "Python"}

# Render with input
rendered = prompt.render(**inputs)
```

### 2. Test with Different Inputs

```python
# Test with 1 example
inputs_1 = grompt.load_input("code-review", "examples-1")
result_1 = prompt.render(**inputs_1)

# Test with 3 examples
inputs_3 = grompt.load_input("code-review", "examples-3")
result_3 = prompt.render(**inputs_3)

# Compare performance
print(f"1 example: {len(result_1)} tokens")
print(f"3 examples: {len(result_3)} tokens")
```

### 3. List Available Inputs

```python
# List all inputs for a prompt
inputs = grompt.list_inputs("code-review")
# Returns: ["simple", "examples-1", "examples-3", "complex"]

# Use in loop
for input_name in inputs:
    test_input = grompt.load_input("code-review", input_name)
    result = prompt.render(**test_input)
    print(f"{input_name}: {len(result)} tokens")
```

### 4. CLI Usage

```bash
# Render with specific input
grompt render code-review --input simple

# Render with input and show output
grompt render code-review --input examples-1

# List available inputs
grompt inputs code-review

# Validate with all inputs
grompt validate code-review --with-inputs
```

---

## Integration with Validation

### Validation with Test Inputs

```bash
$ grompt validate code-review --with-inputs
Validating code-review...

✓ Template syntax: OK
✓ Renders without errors: OK

Testing with inputs:
  ✓ simple: Renders OK (245 tokens)
  ✓ examples-1: Renders OK (512 tokens)
  ✓ examples-3: Renders OK (890 tokens)
  ✓ complex: Renders OK (678 tokens)

✓ All inputs render successfully
```

### Pre-Commit Validation

```bash
$ grompt commit code-review
Running validation...

✓ Template syntax: OK
✓ Renders without errors: OK

Testing with inputs:
  ✓ simple: OK
  ✓ examples-1: OK
  ✓ examples-3: OK
  ✓ complex: OK

✓ All criteria met
✓ Committed (v1 → v2)
```

---

## File Naming Convention

### Pattern

```
{prompt-id}.{input-name}.yaml
```

**Examples**:
- `code-review.simple.yaml`
- `code-review.examples-1.yaml`
- `code-review.examples-3.yaml`
- `code-review.complex.yaml`
- `code-review.edge-case.yaml`

### Rules

1. **Base name**: `{prompt-id}` matches prompt ID
2. **Input name**: `{input-name}` describes the input
3. **Extension**: `.yaml`
4. **Location**: `prompts/test-inputs/` directory

### Why This Works

- **Simple**: Just look at filenames
- **Grouped**: All inputs for a prompt together
- **Tool-friendly**: Easy to glob (`code-review.*.yaml`)
- **Human-readable**: Clear what each input is

---

## Implementation

### 1. Input Loader

**File**: `grompt/infrastructure/storage/input_loader.py` (new)

```python
class InputLoader:
    """Load test inputs from files."""
    
    def __init__(self, inputs_dir: Path = Path("prompts/test-inputs")):
        self.inputs_dir = Path(inputs_dir)
    
    def load_input(self, prompt_id: str, input_name: str) -> Dict[str, Any]:
        """Load a specific input file."""
        path = self.inputs_dir / f"{prompt_id}.{input_name}.yaml"
        if not path.exists():
            raise FileNotFoundError(f"Input file not found: {path}")
        
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
        
        # Remove metadata, return just variables
        metadata_keys = {'description', 'tags', 'metadata'}
        variables = {k: v for k, v in data.items() if k not in metadata_keys}
        
        return variables
    
    def list_inputs(self, prompt_id: str) -> List[str]:
        """List all input names for a prompt."""
        pattern = f"{prompt_id}.*.yaml"
        inputs = []
        
        for file in self.inputs_dir.glob(pattern):
            # Extract input name: code-review.simple.yaml → simple
            stem = file.stem  # code-review.simple
            if stem.startswith(f"{prompt_id}."):
                input_name = stem[len(prompt_id) + 1:]  # simple
                inputs.append(input_name)
        
        return sorted(inputs)
    
    def exists(self, prompt_id: str, input_name: str) -> bool:
        """Check if input file exists."""
        path = self.inputs_dir / f"{prompt_id}.{input_name}.yaml"
        return path.exists()
```

### 2. API Integration

**File**: `grompt/__init__.py` (modify)

```python
def load_input(
    prompt_id: str,
    input_name: str,
    inputs_dir: Union[str, Path] = "prompts/test-inputs"
) -> Dict[str, Any]:
    """
    Load a test input file.
    
    Args:
        prompt_id: The prompt ID
        input_name: The input name (e.g., "simple", "examples-1")
        inputs_dir: Directory containing test inputs
        
    Returns:
        Dictionary of variables to pass to prompt.render()
    """
    loader = InputLoader(inputs_dir=Path(inputs_dir))
    return loader.load_input(prompt_id, input_name)

def list_inputs(
    prompt_id: str,
    inputs_dir: Union[str, Path] = "prompts/test-inputs"
) -> List[str]:
    """
    List all available input names for a prompt.
    
    Args:
        prompt_id: The prompt ID
        inputs_dir: Directory containing test inputs
        
    Returns:
        List of input names
    """
    loader = InputLoader(inputs_dir=Path(inputs_dir))
    return loader.list_inputs(prompt_id)
```

### 3. CLI Commands

**File**: `grompt/application/cli/commands/render.py` (new)

```python
@click.command()
@click.argument('prompt_id')
@click.option('--input', 'input_name', help='Input name to use')
@click.option('--var', multiple=True, help='Override variables (key=value)')
def render(prompt_id: str, input_name: Optional[str], var: tuple) -> None:
    """Render a prompt with test input."""
    prompt = grompt.load(prompt_id)
    
    if input_name:
        # Load from input file
        inputs = grompt.load_input(prompt_id, input_name)
    else:
        inputs = {}
    
    # Override with --var options
    for v in var:
        key, value = v.split('=', 1)
        inputs[key] = value
    
    # Render
    rendered = prompt.render(**inputs)
    click.echo(rendered)
```

**File**: `grompt/application/cli/commands/inputs.py` (new)

```python
@click.command()
@click.argument('prompt_id')
def inputs(prompt_id: str) -> None:
    """List available test inputs for a prompt."""
    input_names = grompt.list_inputs(prompt_id)
    
    if not input_names:
        click.echo(f"No test inputs found for '{prompt_id}'")
        return
    
    click.echo(f"Test inputs for '{prompt_id}':")
    for name in input_names:
        click.echo(f"  - {name}")
```

### 4. Validation Integration

**File**: `grompt/core/validator.py` (modify)

```python
def validate_with_inputs(
    prompt: Prompt,
    inputs_dir: Path = Path("prompts/test-inputs")
) -> ValidationResult:
    """Validate prompt with all test inputs."""
    loader = InputLoader(inputs_dir=inputs_dir)
    input_names = loader.list_inputs(prompt.id)
    
    results = []
    for input_name in input_names:
        try:
            inputs = loader.load_input(prompt.id, input_name)
            rendered = prompt.render(**inputs)
            
            if not rendered:
                results.append(ValidationError(
                    input_name=input_name,
                    error="Empty output"
                ))
            else:
                results.append(ValidationSuccess(
                    input_name=input_name,
                    tokens=len(rendered)  # Approximate
                ))
        except Exception as e:
            results.append(ValidationError(
                input_name=input_name,
                error=str(e)
            ))
    
    return ValidationResult(results)
```

---

## Workflow Examples

### Workflow 1: Testing Few-Shot Efficiency

```bash
# 1. Create prompt
$ grompt add code-review

# 2. Create test inputs
$ cat > prompts/test-inputs/code-review.examples-0.yaml << EOF
code: |
  def divide(x, y):
      return x / y
language: Python
EOF

$ cat > prompts/test-inputs/code-review.examples-1.yaml << EOF
code: |
  def divide(x, y):
      return x / y
language: Python
examples:
  - "Example 1: Error handling"
EOF

$ cat > prompts/test-inputs/code-review.examples-3.yaml << EOF
code: |
  def divide(x, y):
      return x / y
language: Python
examples:
  - "Example 1: Error handling"
  - "Example 2: Type hints"
  - "Example 3: Documentation"
EOF

# 3. Test with different inputs
$ grompt render code-review --input examples-0 | wc -c
$ grompt render code-review --input examples-1 | wc -c
$ grompt render code-review --input examples-3 | wc -c

# 4. Compare performance
```

### Workflow 2: Tracking Performance Over Versions

```python
# test_performance.py
import grompt

def test_performance():
    prompt_v1 = grompt.load("code-review", version=1)
    prompt_v2 = grompt.load("code-review", version=2)
    
    inputs = grompt.list_inputs("code-review")
    
    for input_name in inputs:
        test_input = grompt.load_input("code-review", input_name)
        
        v1_result = prompt_v1.render(**test_input)
        v2_result = prompt_v2.render(**test_input)
        
        print(f"{input_name}:")
        print(f"  v1: {len(v1_result)} chars")
        print(f"  v2: {len(v2_result)} chars")
        print(f"  diff: {len(v2_result) - len(v1_result)} chars")
```

### Workflow 3: Validation with Inputs

```bash
# Validate prompt works with all inputs
$ grompt validate code-review --with-inputs

# Output:
# ✓ Template syntax: OK
# ✓ Renders without errors: OK
# 
# Testing with inputs:
#   ✓ examples-0: OK (245 tokens)
#   ✓ examples-1: OK (512 tokens)
#   ✓ examples-3: OK (890 tokens)
# 
# ✓ All inputs render successfully
```

---

## Directory Structure

```
my-project/
├── prompts/
│   ├── code-review.yaml              ← Prompt
│   ├── summarize.yaml                 ← Prompt
│   └── test-inputs/                  ← Test inputs
│       ├── code-review.simple.yaml
│       ├── code-review.examples-1.yaml
│       ├── code-review.examples-3.yaml
│       ├── summarize.short.yaml
│       └── summarize.long.yaml
│
├── tests/                             ← Pytest tests (optional)
│   └── test_prompts.py
│
└── .grompt/
    └── config.yaml
```

**Simple. Flat. Easy to understand.**

---

## Integration with Criteria

### Criteria Can Reference Inputs

```yaml
# prompts/code-review.yaml
id: code-review
version: 1
template: |
  Review {{ code }}

criteria:
  must:
    - renders_without_errors: true
    - produces_output: true
  
  should:
    - max_tokens: 1000
    - test_with_inputs: ["simple", "examples-1"]  # Test with specific inputs
```

**Validation**:
```bash
$ grompt validate code-review
✓ Template syntax: OK
✓ Renders without errors: OK
✓ Test with 'simple': OK (245 tokens)
✓ Test with 'examples-1': OK (512 tokens)
✓ All criteria met
```

---

## Advanced: Input Collections

### Grouping Related Inputs

```yaml
# prompts/test-inputs/code-review.few-shot.yaml
# Collection of few-shot inputs
inputs:
  - name: examples-0
    code: |
      def divide(x, y):
          return x / y
    language: Python
  
  - name: examples-1
    code: |
      def divide(x, y):
          return x / y
    language: Python
    examples:
      - "Example 1"
  
  - name: examples-3
    code: |
      def divide(x, y):
          return x / y
    language: Python
    examples:
      - "Example 1"
      - "Example 2"
      - "Example 3"
```

**Usage**:
```python
# Load collection
collection = grompt.load_input_collection("code-review", "few-shot")

# Access individual inputs
for input_data in collection['inputs']:
    result = prompt.render(**input_data)
    print(f"{input_data['name']}: {len(result)} tokens")
```

**Note**: This is optional. Simple files are usually enough.

---

## MVP Implementation Plan

### Phase 1: Basic Input Loading

1. **Create InputLoader** (`grompt/infrastructure/storage/input_loader.py`)
   - Load input files
   - List available inputs
   - Simple file-based approach

2. **Add API Functions** (`grompt/__init__.py`)
   - `load_input(prompt_id, input_name)`
   - `list_inputs(prompt_id)`

3. **Add CLI Commands** (optional)
   - `grompt render <id> --input <name>`
   - `grompt inputs <id>`

### Phase 2: Validation Integration

4. **Integrate with Validator**
   - Validate prompt with all inputs
   - Check all inputs render successfully
   - Report token counts

5. **Pre-Commit Validation**
   - Test all inputs before committing
   - Ensure no regressions

### Phase 3: Performance Tracking (Future)

6. **Track Performance**
   - Compare versions with same inputs
   - Track token counts over time
   - Generate reports

---

## File Format Details

### Required Fields

**None!** Input files are just variable dictionaries.

### Optional Metadata

```yaml
# Metadata (optional, ignored when loading)
description: Simple function example
tags: [simple, basic]
created: 2024-01-15

# Variables (used for rendering)
code: |
  def add(a, b):
      return a + b
language: Python
```

**Metadata is ignored** when loading inputs. Only variables are returned.

---

## Examples

### Example 1: Few-Shot Testing

```bash
# Create inputs
$ cat > prompts/test-inputs/code-review.no-examples.yaml << EOF
code: |
  def divide(x, y):
      return x / y
language: Python
EOF

$ cat > prompts/test-inputs/code-review.with-examples.yaml << EOF
code: |
  def divide(x, y):
      return x / y
language: Python
examples:
  - "Example: Good error handling"
  - "Example: Type hints"
EOF

# Test both
$ grompt render code-review --input no-examples
$ grompt render code-review --input with-examples

# Compare
python3 << EOF
import grompt
prompt = grompt.load("code-review")

no_examples = grompt.load_input("code-review", "no-examples")
with_examples = grompt.load_input("code-review", "with-examples")

result1 = prompt.render(**no_examples)
result2 = prompt.render(**with_examples)

print(f"No examples: {len(result1)} chars")
print(f"With examples: {len(result2)} chars")
EOF
```

### Example 2: Edge Case Testing

```yaml
# prompts/test-inputs/code-review.empty.yaml
code: ""
language: Python

# prompts/test-inputs/code-review.very-long.yaml
code: |
  # Very long code file...
  # ... hundreds of lines ...
language: Python
```

### Example 3: Different Languages

```yaml
# prompts/test-inputs/code-review.python.yaml
code: |
  def add(a, b):
      return a + b
language: Python

# prompts/test-inputs/code-review.javascript.yaml
code: |
  function add(a, b) {
      return a + b;
  }
language: JavaScript
```

---

## Summary

**Test inputs are just files:**

- **Location**: `prompts/test-inputs/{prompt-id}.{name}.yaml`
- **Format**: YAML with variables
- **Usage**: `grompt.load_input("code-review", "simple")`
- **Integration**: Works with validation, testing, performance tracking

**Benefits**:
- ✅ Store well-known inputs
- ✅ Test with different configurations
- ✅ Track performance over versions
- ✅ Simple: Just files, no database
- ✅ Version-controlled: Track inputs with git

**MVP**:
1. InputLoader class
2. `load_input()` and `list_inputs()` API
3. Integration with validation
4. Optional CLI commands

**That's it.** Simple, file-based, plug-and-play.

