# Flexible Input System: Don't Enforce Structure

## The Question

Should we enforce a specific test-input folder structure, or just enable flexible input substitution?

**Answer: Keep it flexible. Don't enforce structure.**

---

## The Simple Approach

### Core Principle

**Grompt doesn't care where inputs come from.** Just provide variables when rendering.

### Current API (Already Works)

```python
import grompt

prompt = grompt.load("code-review")

# Direct variables
result = prompt.render(code="def add(a, b): return a + b", language="Python")

# From dict
variables = {"code": "...", "language": "Python"}
result = prompt.render(**variables)
```

**This already works.** No changes needed.

---

## Optional: Load Variables from Files

### Simple Helper (Optional)

**Don't enforce structure.** Just provide a helper to load YAML files.

```python
# grompt/utils.py (optional helper)
def load_variables(file_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Load variables from a YAML file.
    
    Users can organize files however they want:
    - inputs/code-review-simple.yaml
    - test-data/code-review.yaml
    - fixtures/inputs.yaml
    - Anywhere, any name
    """
    import yaml
    with open(file_path, 'r') as f:
        return yaml.safe_load(f) or {}
```

### Usage (Flexible)

```python
import grompt
from grompt.utils import load_variables  # Optional helper

prompt = grompt.load("code-review")

# Option 1: Direct variables
result = prompt.render(code="...", language="Python")

# Option 2: From file (anywhere, any name)
variables = load_variables("inputs/simple.yaml")
result = prompt.render(**variables)

# Option 3: From file (different location)
variables = load_variables("test-data/code-review.yaml")
result = prompt.render(**variables)

# Option 4: From file URI (future)
variables = load_variables("file://inputs/simple.yaml")
result = prompt.render(**variables)
```

**No enforced structure.** Users organize files however they want.

---

## File URI Support (Future, Optional)

### Simple URI Parsing

```python
def load_variables(source: Union[str, Path]) -> Dict[str, Any]:
    """
    Load variables from file path or URI.
    
    Supports:
    - "inputs/simple.yaml" (relative path)
    - "/absolute/path/inputs.yaml" (absolute path)
    - "file://inputs/simple.yaml" (file URI, optional)
    """
    # Handle file:// URI
    if source.startswith("file://"):
        source = source[7:]  # Remove file:// prefix
    
    # Load YAML
    with open(source, 'r') as f:
        return yaml.safe_load(f) or {}
```

**Keep it simple.** Just file paths, URI is optional sugar.

---

## What Users Can Do (No Enforcement)

### Option 1: No Input Files
```python
# Just pass variables directly
prompt.render(code="...", language="Python")
```

### Option 2: Organize However They Want
```
my-project/
├── prompts/
│   └── code-review.yaml
├── inputs/                    ← User's choice
│   └── simple.yaml
├── test-data/                ← Or here
│   └── code-review.yaml
└── fixtures/                 ← Or here
    └── inputs.yaml
```

### Option 3: Use pytest fixtures
```python
# tests/conftest.py
import pytest
import yaml

@pytest.fixture
def simple_inputs():
    with open("inputs/simple.yaml") as f:
        return yaml.safe_load(f)

def test_code_review(simple_inputs):
    prompt = grompt.load("code-review")
    result = prompt.render(**simple_inputs)
    assert result
```

**Grompt doesn't care.** Just provide variables.

---

## Comparison: Enforced vs Flexible

### Enforced Structure (What We Designed)

```
prompts/
├── code-review.yaml
└── test-inputs/              ← Enforced location
    └── code-review.simple.yaml  ← Enforced naming
```

**Pros**:
- Consistent across projects
- Easy to discover inputs
- `grompt.load_input()` convenience

**Cons**:
- ❌ Enforces structure (against "just files" philosophy)
- ❌ Less flexible
- ❌ Users might already have input files elsewhere
- ❌ More code to maintain

### Flexible Approach (Recommended)

```
# Users organize however they want
inputs/simple.yaml
test-data/code-review.yaml
fixtures/inputs.yaml
anywhere/any-name.yaml
```

**Pros**:
- ✅ No enforced structure
- ✅ Maximum flexibility
- ✅ Works with existing workflows
- ✅ Minimal code (just a helper function)
- ✅ Aligns with "just files" philosophy

**Cons**:
- Users need to know file paths
- No `grompt.load_input()` convenience (but not needed)

---

## Recommendation: Flexible Approach

### What to Provide

**1. Core API (Already Works)**
```python
prompt.render(**variables)  # Already works, no changes
```

**2. Optional Helper (Simple)**
```python
# grompt/utils.py (optional, not required)
def load_variables(file_path: Union[str, Path]) -> Dict[str, Any]:
    """Load variables from YAML file. Users organize files however they want."""
    import yaml
    with open(file_path, 'r') as f:
        return yaml.safe_load(f) or {}
```

**3. Documentation**
- Show how to load from files (any location)
- Show pytest examples
- Show different organizational patterns

**That's it.** No enforced structure, just flexibility.

---

## Implementation

### Minimal: Just Helper Function

**File**: `grompt/utils.py` (new, optional)

```python
"""
Utility functions for working with prompts.
Optional helpers - not required for core functionality.
"""

from pathlib import Path
from typing import Dict, Any, Union
import yaml


def load_variables(file_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Load variables from a YAML file.
    
    Users can organize files however they want - this function
    doesn't enforce any structure.
    
    Args:
        file_path: Path to YAML file (relative or absolute)
        
    Returns:
        Dictionary of variables
        
    Example:
        variables = load_variables("inputs/simple.yaml")
        prompt.render(**variables)
    """
    path = Path(file_path)
    
    # Handle file:// URI (optional)
    if isinstance(file_path, str) and file_path.startswith("file://"):
        path = Path(file_path[7:])
    
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")
    
    with open(path, 'r') as f:
        data = yaml.safe_load(f)
    
    return data or {}
```

**Usage**:
```python
import grompt
from grompt.utils import load_variables  # Optional

prompt = grompt.load("code-review")

# Load from anywhere
variables = load_variables("inputs/simple.yaml")
result = prompt.render(**variables)
```

### No Enforced Structure

**Don't create**:
- ❌ `InputLoader` class
- ❌ `prompts/test-inputs/` folder structure
- ❌ `grompt.load_input()` API
- ❌ `grompt.list_inputs()` API

**Just provide**:
- ✅ `load_variables()` helper (optional)
- ✅ Documentation showing flexibility

---

## Examples: Different Organizational Patterns

### Pattern 1: Simple Inputs Folder

```
my-project/
├── prompts/
│   └── code-review.yaml
└── inputs/                    ← User's choice
    ├── simple.yaml
    └── complex.yaml
```

```python
variables = load_variables("inputs/simple.yaml")
prompt.render(**variables)
```

### Pattern 2: Test Data Folder

```
my-project/
├── prompts/
│   └── code-review.yaml
└── test-data/                 ← User's choice
    └── code-review.yaml
```

```python
variables = load_variables("test-data/code-review.yaml")
prompt.render(**variables)
```

### Pattern 3: Pytest Fixtures

```
my-project/
├── prompts/
│   └── code-review.yaml
└── tests/
    ├── conftest.py
    └── fixtures/
        └── inputs.yaml
```

```python
# tests/conftest.py
@pytest.fixture
def test_inputs():
    return load_variables("tests/fixtures/inputs.yaml")

# tests/test_prompts.py
def test_code_review(test_inputs):
    prompt = grompt.load("code-review")
    result = prompt.render(**test_inputs)
    assert result
```

### Pattern 4: Per-Prompt Inputs

```
my-project/
├── prompts/
│   ├── code-review.yaml
│   └── code-review-inputs/    ← User's choice
│       ├── simple.yaml
│       └── complex.yaml
```

```python
variables = load_variables("prompts/code-review-inputs/simple.yaml")
prompt.render(**variables)
```

**All valid.** Grompt doesn't care.

---

## Few-Shot Example (Flexible)

### User's Input Files (Anywhere)

```yaml
# inputs/examples-1.yaml (user's choice of location/name)
code: |
  def divide(x, y):
      return x / y
language: Python
examples:
  - "Example 1: Error handling"
```

```yaml
# inputs/examples-3.yaml
code: |
  def divide(x, y):
      return x / y
language: Python
examples:
  - "Example 1: Error handling"
  - "Example 2: Type hints"
  - "Example 3: Documentation"
```

### Usage

```python
import grompt
from grompt.utils import load_variables

prompt = grompt.load("code-review")

# Test with 1 example
inputs_1 = load_variables("inputs/examples-1.yaml")
result_1 = prompt.render(**inputs_1)

# Test with 3 examples
inputs_3 = load_variables("inputs/examples-3.yaml")
result_3 = prompt.render(**inputs_3)

# Compare
print(f"1 example: {len(result_1)} chars")
print(f"3 examples: {len(result_3)} chars")
```

**No enforced structure.** Users organize files however they want.

---

## Integration with Validation

### Validation with User's Input Files

```python
# User defines which inputs to test
test_inputs = [
    "inputs/simple.yaml",
    "inputs/complex.yaml",
    "test-data/edge-cases.yaml"
]

for input_file in test_inputs:
    variables = load_variables(input_file)
    result = prompt.render(**variables)
    assert result  # Non-empty
```

**Or in prompt metadata** (optional):

```yaml
# prompts/code-review.yaml
id: code-review
version: 1
template: |
  Review {{ code }}

# Optional: Reference input files (not enforced)
test_inputs:
  - "inputs/simple.yaml"
  - "inputs/complex.yaml"
```

**Validation uses these files** (if provided), but doesn't enforce structure.

---

## CLI Usage (Optional)

### Render with Input File

```bash
# Render with input file (any path)
grompt render code-review --input inputs/simple.yaml

# Or with variables directly
grompt render code-review --var code="..." --var language="Python"
```

**Both work.** No enforced structure.

---

## Summary: Flexible Approach

### What Grompt Provides

1. **Core API** (already works):
   ```python
   prompt.render(**variables)
   ```

2. **Optional Helper** (simple):
   ```python
   load_variables(file_path)  # Load from any file, anywhere
   ```

3. **Documentation**:
   - Show different organizational patterns
   - Show pytest examples
   - Show flexibility

### What Grompt Doesn't Do

- ❌ Enforce folder structure
- ❌ Enforce naming conventions
- ❌ Create `prompts/test-inputs/` automatically
- ❌ Provide `load_input()` convenience API

### Why This Works

- ✅ **Flexible**: Users organize however they want
- ✅ **Simple**: Just a helper function
- ✅ **Familiar**: Works with existing workflows
- ✅ **Powerful**: Can use with pytest, any testing framework
- ✅ **Aligned**: Matches "just files" philosophy

---

## Updated MVP

### What to Build

1. ✅ **Core API** (already works - `prompt.render(**kwargs)`)
2. ⚠️ **Optional helper** (`load_variables()` - simple function)
3. ⚠️ **Documentation** (show flexibility)

**That's it.** No enforced structure, just enable the capability.

---

## Recommendation

**Don't enforce test-input structure.** Just provide:

1. **Core API** (already exists)
2. **Optional helper** (`load_variables()`)
3. **Documentation** (show flexibility)

**Users organize files however they want.** Grompt just loads them.

**This aligns with "Keep It Stupid Simple" and "just files" philosophy.**

