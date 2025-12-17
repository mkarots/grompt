# Validation and Guardrails: Is Grompt Complete Without Them?

## The Core Question

**Is versioning + decoupling enough, or do we need validation/guardrails?**

Versioning broken prompts isn't useful. You need some way to ensure prompts work correctly.

---

## The Problem: Versioning Without Validation

### What Happens Without Validation

```
Day 1: Create prompt v1 → Works great
Day 2: Edit prompt → Create v2 → Broken (typo, wrong variable)
Day 3: Deploy v2 → Production breaks
Day 4: Realize v2 is broken → Rollback to v1
```

**Without validation, you're just versioning broken prompts.**

### Real-World Scenarios

1. **Template syntax errors**: `{{ unclosed` → Runtime error
2. **Missing variables**: Template expects `{{ code }}` but gets nothing
3. **Wrong variable names**: Template uses `{{ code }}` but you pass `{{ source }}`
4. **Broken logic**: Jinja2 conditionals that always fail
5. **Empty output**: Prompt renders but produces empty string
6. **Regression**: v2 works but doesn't meet v1's criteria

---

## What "Complete" Means

### Minimal Completeness (MVP)

**Must have**:
1. ✅ Versioning (done)
2. ✅ Decoupling from code (done)
3. ⚠️ **Syntax validation** (missing - template renders without errors)
4. ⚠️ **Basic sanity checks** (missing - produces non-empty output)
5. ⚠️ **Test inputs** (missing - store well-known inputs for testing)

**Without these, grompt is incomplete.**

**Why test inputs matter**:
- Need well-known inputs to test prompts consistently
- Track performance across versions
- Experiment with different configurations (e.g., few-shot examples)
- Validate prompts work with real data

### Full Completeness (Production Ready)

**Should have**:
5. ⚠️ **Variable validation** (missing - required vars provided)
6. ⚠️ **Criteria/guardrails** (missing - define what "good" means)
7. ⚠️ **Regression prevention** (missing - ensure v2 meets v1's criteria)

---

## Option A: Minimal Validation (Recommended for MVP)

### What It Includes

**1. Syntax Validation**
- Template renders without Jinja2 errors
- All variables are defined (or have defaults)
- No syntax errors

**2. Basic Sanity Checks**
- Template produces non-empty output
- Required variables are provided
- Template structure is valid

**3. Criteria Definition (Lightweight)**
- Define "must have" criteria in prompt metadata
- Validate criteria are met before commit
- MoSCoW-style: Must, Should, Could, Won't

### Implementation

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
    - includes_variable: ["code"]
  
  should:
    - output_contains: ["review", "code"]
    - max_tokens: 500
  
  could:
    - output_length: "> 100"
```

**Validation Command**:
```bash
$ grompt validate code-review
✓ Template syntax: OK
✓ Renders without errors: OK
✓ Produces output: OK
✓ Must criteria: 3/3 passed
✓ Should criteria: 2/2 passed
⚠ Could criteria: 1/1 passed (optional)

$ grompt commit code-review
✓ All criteria met, committing...
```

### Pros

- ✅ **Prevents broken prompts**: Catches syntax errors before commit
- ✅ **Lightweight**: No test runner, just validation
- ✅ **MoSCoW support**: Define what "good" means
- ✅ **Prevents regressions**: Can compare v2 against v1 criteria
- ✅ **Simple**: Just metadata + validation logic

### Cons

- ❌ **Not full testing**: Doesn't test LLM output quality
- ❌ **Static checks only**: Can't verify semantic correctness
- ❌ **Limited assertions**: Can't check complex conditions

---

## Option B: Full Test Runner (Future)

### What It Includes

Everything from Option A, plus:
- Test cases with expected outputs
- LLM execution and evaluation
- Assertions on LLM responses
- Comparison between versions

**This is what we discussed earlier - probably overkill for MVP.**

---

## Option C: Hybrid - Validation + Programmatic Testing

### What It Includes

**Built-in (Lightweight)**:
- Syntax validation
- Basic sanity checks
- Criteria definition (MoSCoW)
- Guardrails (must criteria enforced)

**Programmatic (User-provided)**:
- Full test suites with pytest
- LLM output evaluation
- Complex assertions
- Integration tests

### How It Works

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
    - max_tokens: 500
```

```python
# tests/test_code_review.py (user-written)
import grompt

def test_code_review_quality():
    """User-defined quality tests."""
    prompt = grompt.load("code-review")
    result = prompt.render(code="def add(a, b): return a + b")
    
    # User's quality criteria
    assert "function" in result.lower()
    assert len(result) < 500
```

**Validation runs automatically**:
```bash
$ grompt commit code-review
Running validation...
✓ Syntax: OK
✓ Must criteria: 2/2 passed
✓ Should criteria: 1/1 passed
✓ Committed (v1 → v2)
```

**User tests run separately**:
```bash
$ pytest tests/test_code_review.py
```

---

## Recommendation: Option C (Hybrid)

### Why This Works

1. **Prevents broken prompts**: Built-in validation catches syntax errors
2. **Defines criteria**: MoSCoW-style guardrails ensure quality
3. **Prevents regressions**: Can compare versions against criteria
4. **Keeps it simple**: No test runner, just validation + criteria
5. **Enables advanced testing**: Users can write pytest tests for quality

### What to Implement

#### Phase 1: Basic Validation (MVP)

**1. Syntax Validation**
```python
def validate_template(prompt: Prompt) -> ValidationResult:
    """Validate template syntax and basic structure."""
    # Check Jinja2 syntax
    # Check required variables
    # Check template renders
    pass
```

**2. Criteria Definition**
```yaml
criteria:
  must:
    - renders_without_errors: true
    - produces_output: true
  should:
    - max_tokens: 500
```

**3. Validation Command**
```bash
grompt validate code-review
```

**4. Pre-commit Validation**
```bash
grompt commit code-review  # Automatically validates before committing
```

#### Phase 2: Criteria Enforcement (Future)

**1. MoSCoW Criteria**
- Must: Block commit if failed
- Should: Warn if failed
- Could: Info if failed

**2. Version Comparison**
- Compare v2 against v1's criteria
- Ensure no regressions

**3. Guardrails**
- Enforce must criteria
- Optional should/could criteria

---

## What "Complete" Means: Revised

### MVP Completeness

**Must have**:
1. ✅ Versioning
2. ✅ Decoupling from code
3. ⚠️ **Syntax validation** (prevents broken templates)
4. ⚠️ **Basic criteria** (defines what "good" means)

**Without #3 and #4, grompt is incomplete.**

### Production Completeness

**Should have**:
5. ⚠️ **Criteria enforcement** (must/should/could)
6. ⚠️ **Regression prevention** (compare versions)
7. ⚠️ **Programmatic testing support** (pytest examples)

---

## Implementation Plan

### Step 1: Add Test Inputs (Critical)

**File**: `grompt/infrastructure/storage/input_loader.py` (new)

```python
class InputLoader:
    """Load test inputs from files."""
    
    def load_input(self, prompt_id: str, input_name: str) -> Dict[str, Any]:
        """Load input file: prompts/test-inputs/{prompt_id}.{input_name}.yaml"""
        pass
    
    def list_inputs(self, prompt_id: str) -> List[str]:
        """List all input names for a prompt."""
        pass
```

**File**: `grompt/__init__.py` (modify)

```python
def load_input(prompt_id: str, input_name: str) -> Dict[str, Any]:
    """Load test input file."""
    pass

def list_inputs(prompt_id: str) -> List[str]:
    """List available test inputs."""
    pass
```

**Why first**: Need inputs before we can validate with real data.

### Step 2: Add Validation (Critical)

**File**: `grompt/core/validator.py` (new)

```python
class PromptValidator:
    @staticmethod
    def validate_syntax(prompt: Prompt) -> ValidationResult:
        """Check template syntax."""
        pass
    
    @staticmethod
    def validate_renders(prompt: Prompt, variables: Dict) -> ValidationResult:
        """Check template renders without errors."""
        pass
    
    @staticmethod
    def validate_with_inputs(prompt: Prompt) -> ValidationResult:
        """Validate prompt with all test inputs."""
        pass
    
    @staticmethod
    def validate_criteria(prompt: Prompt, criteria: Dict) -> ValidationResult:
        """Check criteria are met."""
        pass
```

### Step 2: Add Criteria Support

**File**: `grompt/core/prompt.py` (modify)

```python
@dataclass
class Prompt:
    # ... existing fields ...
    criteria: Optional[Dict[str, Any]] = None  # New field
```

**YAML Format**:
```yaml
criteria:
  must:
    - renders_without_errors: true
    - produces_output: true
  should:
    - max_tokens: 500
```

### Step 3: Add Validation Command

**File**: `grompt/application/cli/commands/validate.py` (new)

```python
@click.command()
@click.argument('name')
def validate(name: str) -> None:
    """Validate prompt syntax and criteria."""
    prompt = loader.load_prompt(name)
    result = PromptValidator.validate(prompt)
    # Display results
```

### Step 4: Integrate with Commit

**File**: `grompt/application/cli/commands/commit.py` (modify)

```python
def commit(name: str, message: Optional[str]) -> None:
    prompt = loader.load_prompt(prompt_id)
    
    # Validate before committing
    validation_result = PromptValidator.validate(prompt)
    if not validation_result.passed:
        click.echo("Validation failed. Fix errors before committing.")
        return
    
    # ... rest of commit logic
```

---

## Criteria Examples

### Example 1: Code Review Prompt

```yaml
criteria:
  must:
    - renders_without_errors: true
    - produces_output: true
    - includes_variable: ["code"]
  
  should:
    - output_contains: ["review", "code"]
    - max_tokens: 1000
  
  could:
    - output_length: "> 200"
```

### Example 2: Summarization Prompt

```yaml
criteria:
  must:
    - renders_without_errors: true
    - produces_output: true
    - includes_variable: ["text"]
  
  should:
    - output_length: "< 500"
    - output_contains: ["summary"]
  
  could:
    - sentence_count: "<= 3"
```

### Example 3: Translation Prompt

```yaml
criteria:
  must:
    - renders_without_errors: true
    - produces_output: true
    - includes_variable: ["text", "target_language"]
  
  should:
    - output_contains: ["{{ target_language }}"]
    - max_tokens: 2000
```

---

## MoSCoW Criteria Format

### Structure

```yaml
criteria:
  must:      # Block commit if failed
    - condition: value
  
  should:    # Warn if failed
    - condition: value
  
  could:     # Info if failed
    - condition: value
  
  wont:      # Not checked, just documented
    - condition: value
```

### Supported Conditions

**Basic**:
- `renders_without_errors: true`
- `produces_output: true`
- `includes_variable: ["var1", "var2"]`

**Output Checks**:
- `output_contains: ["keyword1", "keyword2"]`
- `output_length: "> 100"` or `"< 500"`
- `max_tokens: 500`
- `sentence_count: "<= 3"`

**Custom** (future):
- `custom_check: "python_function_name"`

---

## Answer: Is Grompt Complete?

### Without Validation: **No**

**Missing**:
- Way to ensure prompts work
- Way to prevent broken prompts
- Way to define quality criteria

**Result**: You're just versioning potentially broken prompts.

### With Minimal Validation: **Yes (MVP)**

**Includes**:
- Syntax validation
- Basic sanity checks
- Criteria definition (MoSCoW)
- Pre-commit validation

**Result**: Can ensure prompts work before committing.

### With Full Testing: **Yes (Production)**

**Includes**:
- Everything above
- Programmatic testing support
- LLM output evaluation (user-provided)
- Regression prevention

**Result**: Complete solution for production use.

---

## Recommendation

**Implement minimal validation (Option C - Hybrid)**:

1. **Syntax validation** (critical)
2. **Criteria definition** (MoSCoW)
3. **Pre-commit validation** (enforce must criteria)
4. **Programmatic testing** (pytest examples, not built-in runner)

**Why**:
- Prevents broken prompts (essential)
- Defines quality criteria (MoSCoW)
- Keeps it simple (no test runner)
- Enables advanced testing (pytest)

**Timeline**:
- **Now**: Add syntax validation + basic criteria
- **Later**: Add criteria enforcement + regression prevention
- **Future**: Add programmatic testing examples

---

## Summary

**You're right**: Grompt is incomplete without validation/guardrails.

**Solution**: Minimal validation + criteria (MoSCoW) + programmatic testing.

**Not needed**: Full test runner (too complex, use pytest instead).

**MVP**: Syntax validation + criteria definition + pre-commit checks.

