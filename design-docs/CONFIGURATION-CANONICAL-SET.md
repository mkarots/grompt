
# Configuration Canonical Set

## Overview

The Grompt test case system needs a **canonical set of configuration** - a minimal, non-redundant set of configuration options that can express all possible test scenarios without ambiguity or duplication.

This document defines the canonical configuration hierarchy, ensuring:
- **Complete**: Can express all needed scenarios including composition, custom functions, and conditional execution
- **Minimal**: No redundant or overlapping options
- **Unambiguous**: Clear precedence and resolution rules
- **Composable**: Options combine predictably with test case references and suite includes
- **Conditional**: Tests can be scoped to run only under specific conditions

---

## Current Capabilities Verified

From TEST-CASE-SYSTEM.md, the system supports:

✅ **Test Case Composition** (lines 60-90, 299-355)
- Reference test cases from other files: `ref: "tests/common/edge-cases.yaml#division_by_zero"`
- Include entire suites: `includes: ["tests/suites/security.yaml"]`
- Override properties when referencing: `ref: "..." + weight: 2.0`

✅ **Custom Evaluator Functions** (lines 225-239)
- Custom evaluator classes: `evaluator_class: "my_package.MyEvaluator"`
- Custom evaluator arguments: `evaluator_args: {threshold: 0.8}`

✅ **Multiple Evaluation Methods** (lines 123-239)
- Semantic, API, Criteria, Regex, Custom

✅ **Model-Specific Testing** (lines 611-869)
- Per-test model selection
- Model groups
- Model-specific expectations

**NEW**: Conditional Execution (to be added)
- Run tests only in specific scopes (CI, local, production)
- Skip tests based on conditions
- Enable/disable tests based on environment

---

## Conditional Execution

### Use Cases

1. **Environment-Specific Tests**
   - Run expensive tests only in CI
   - Skip slow tests during local development
   - Run security tests only in production validation

2. **Feature Flags**
   - Enable/disable tests based on feature availability
   - Test different code paths conditionally

3. **Resource Availability**
   - Skip tests requiring external APIs when offline
   - Run tests only when specific models are available

4. **Development Workflow**
   - Quick smoke tests for rapid iteration
   - Comprehensive tests for pre-commit
   - Full regression suite for CI/CD

### Conditional Syntax

```yaml
test_cases:
  # Run only in CI environment
  - name: "expensive_test"
    when:
      scope: ["ci", "production"]
    input: {...}
  
  # Skip in specific environments
  - name: "local_only_test"
    when:
      not_scope: ["ci"]
    input: {...}
  
  # Run only when condition is met
  - name: "feature_test"
    when:
      env:
        FEATURE_X_ENABLED: "true"
    input: {...}
  
  # Complex conditions
  - name: "conditional_test"
    when:
      any:
        - scope: ["ci"]
        - env:
            DEBUG: "true"
    input: {...}
  
  # Always skip (for debugging)
  - name: "broken_test"
    skip: true
    skip_reason: "Known issue #123"
    input: {...}
```

---

## The Configuration Hierarchy Problem

### Complexity Sources

Configuration can be specified at multiple levels AND composed from multiple sources:

```yaml
# Global config (.grompt)
scopes:
  ci:
    description: "Continuous Integration"
    env:
      CI: "true"
  local:
    description: "Local development"
  production:
    description: "Production validation"

eval:
  default_method: "semantic"
  methods:
    semantic:
      model: "gpt-4"
      threshold: 0.8

# Shared test cases (tests/common/edge-cases.yaml)
test_cases:
  - name: "division_by_zero"
    when:
      scope: ["ci", "production"]  # Don't run locally
    eval_method: "api"
    eval_config:
      api_url: "https://example.com"

# Prompt file (prompts/code-review.yaml)
id: code-review
eval_method: "semantic"
eval_config:
  threshold: 0.9

# Test suite (tests/suites/security.yaml)
name: "security"
when:
  scope: ["ci", "production"]  # Entire suite conditional
eval_method: "criteria"
includes:
  - "tests/suites/base.yaml"
test_cases:
  - ref: "tests/common/edge-cases.yaml#division_by_zero"
    weight: 2.0
```

**Questions:**
- When referencing a test case, which conditions apply?
- Do suite-level conditions override test-level conditions?
- How do conditions interact with includes?
- Can conditions be overridden when referencing?

---

## Canonical Configuration Hierarchy

### Principle: Explicit Composition with Clear Override Rules

Each configuration option has a **clear resolution order** that accounts for:
1. Direct specification (highest priority)
2. Reference source
3. Container defaults (suite/prompt)
4. Global defaults (lowest priority)

### The Five Configuration Levels

```
1. System Defaults (hardcoded in code)
   ↓
2. Global Config (.grompt) - Scope definitions
   ↓
3. Shared Test Definitions (tests/common/*.yaml)
   ↓
4. Prompt/Suite Defaults (prompts/*.yaml, tests/suites/*.yaml)
   ↓
5. Test Case Overrides (inline or via ref with overrides)
```

---

## Configuration Categories

### Category A: System-Level Only

These exist **only** in `.grompt` and cannot be overridden:

```yaml
# .grompt
version: 1
prompts_dir: prompts
tests_dir: tests
cache_dir: .grompt/cache

# Scope definitions (system-level only)
scopes:
  local:
    description: "Local development"
    default: true  # Default scope if none specified
  
  ci:
    description: "Continuous Integration"
    env:
      CI: "true"
  
  production:
    description: "Production validation"
    env:
      PRODUCTION: "true"
  
  quick:
    description: "Quick smoke tests"
    max_duration: 5  # seconds
  
  comprehensive:
    description: "Full test suite"

# Model definitions
models:
  gpt-4:
    provider: openai
    api_key_env: OPENAI_API_KEY
    max_tokens: 8192

# Model groups
model_groups:
  openai: ["gpt-4", "gpt-3.5-turbo"]
  all: ["gpt-4", "gpt-3.5-turbo", "claude-3-opus"]

# Evaluator registry (for custom evaluators)
evaluators:
  custom_security:
    class: "my_package.SecurityEvaluator"
    default_args:
      strict_mode: true
```

**Rule**: Cannot be overridden at any lower level.

### Category B: Shared Test Definitions

Reusable test cases that can be referenced:

```yaml
# tests/common/edge-cases.yaml
test_cases:
  - name: "division_by_zero"
    weight: 1.0
    when:
      scope: ["ci", "production"]  # Condition travels with test
    eval_method: "semantic"
    eval_config:
      threshold: 0.8
    input:
      code: "def calc(x,y): return x/y"
    expected_meaning:
      - "warns about division by zero"
  
  - name: "quick_check"
    when:
      scope: ["local", "quick"]
    eval_method: "regex"
    input: {...}
```

**Rule**: Conditions are part of the test definition and travel with references.

### Category C: Container Defaults

Defaults set at prompt or suite level:

```yaml
# prompts/code-review.yaml
id: code-review
model: gpt-4

# Container-level defaults
eval_method: "semantic"
eval_config:
  threshold: 0.85

# Container-level condition (applies to all inline tests)
when:
  scope: ["ci", "production"]

test_cases:
  - name: "test1"  # Inherits container condition
    input: {...}
  
  - name: "test2"
    when:
      scope: ["local"]  # Override container condition
    input: {...}
```

```yaml
# tests/suites/security.yaml
name: "security"

# Suite-level condition
when:
  scope: ["ci", "production"]

# Suite-level defaults
eval_method: "api"
eval_config:
  api_url: "https://security-eval.example.com"

test_cases:
  - ref: "tests/common/edge-cases.yaml#division_by_zero"
    # Inherits both suite condition AND reference condition (combined with AND)
```

**Rule**: Container conditions apply to inline tests; referenced tests keep their conditions but may be combined.

### Category D: Test-Level Overrides

Final authority for a specific test:

```yaml
test_cases:
  - name: "test1"
    when:
      scope: ["ci"]
    eval_method: "custom"
    eval_config:
      evaluator_class: "my_package.MyEvaluator"
      threshold: 0.95
  
  - name: "test2"
    skip: true
    skip_reason: "Temporarily disabled due to API issues"
```

---

## Conditional Execution Rules

### Rule 1: Condition Types

```yaml
# Scope-based (most common)
when:
  scope: ["ci", "production"]  # Run in these scopes
  not_scope: ["local"]  # Don't run in these scopes

# Environment variable-based
when:
  env:
    FEATURE_X: "true"
    API_KEY: "*"  # Any non-empty value

# Model availability
when:
  models_available: ["gpt-4", "claude-3-opus"]

# Complex conditions
when:
  all:  # AND logic
    - scope: ["ci"]
    - env:
        API_KEY: "*"
  
when:
  any:  # OR logic
    - scope: ["ci"]
    - env:
        DEBUG: "true"

# Skip unconditionally
skip: true
skip_reason: "Known issue #123"
```

### Rule 2: Condition Inheritance for Inline Tests

Inline tests inherit container conditions:

```yaml
# prompts/code-review.yaml
when:
  scope: ["ci"]  # Container condition

test_cases:
  - name: "test1"
    # Inherits: scope=["ci"]
    input: {...}
  
  - name: "test2"
    when:
      scope: ["local"]  # REPLACES container condition
    input: {...}
  
  - name: "test3"
    when:
      all:
        - scope: ["ci"]  # Keep container condition
        - env:
            VERBOSE: "true"  # Add additional condition
    input: {...}
```

### Rule 3: Condition Preservation for References

Referenced tests keep their conditions:

```yaml
# tests/common/security.yaml
test_cases:
  - name: "sql_injection"
    when:
      scope: ["ci", "production"]
    input: {...}

# tests/suites/comprehensive.yaml
when:
  scope: ["ci"]  # Suite condition

test_cases:
  - ref: "tests/common/security.yaml#sql_injection"
    # Effective condition: scope=["ci"] AND scope=["ci", "production"]
    # Result: scope=["ci"] (intersection)
```

**Condition Combination Logic:**
- Suite condition AND reference condition
- Intersection of scopes
- Union of env requirements

### Rule 4: Condition Override Syntax

To override a referenced test's condition:

```yaml
test_cases:
  - ref: "tests/common/security.yaml#sql_injection"
    when:
      scope: ["local"]  # Override reference condition
      override_conditions: true  # Explicit flag
```

Without `override_conditions: true`, conditions are combined (AND logic).

### Rule 5: Skip Takes Precedence

```yaml
test_cases:
  - name: "test1"
    skip: true  # Always skipped, regardless of when conditions
    when:
      scope: ["ci"]  # Ignored
```

---

## Complete Resolution Algorithm

```python
def should_run_test(test_case, container, current_scope, env_vars):
    """
    Determine if a test should run based on conditions.
    
    Args:
        test_case: TestCase object
        container: Prompt or TestSuite containing the test
        current_scope: Current execution scope (e.g., "ci", "local")
        env_vars: Environment variables dict
    
    Returns:
        (should_run: bool, reason: str)
    """
    
    # Check explicit skip
    if test_case.skip:
        return False, test_case.skip_reason or "Explicitly skipped"
    
    # Collect all conditions
    conditions = []
    
    # Container condition (for inline tests only)
    if not test_case.is_reference and container.when:
        conditions.append(container.when)
    
    # Test case condition
    if test_case.when:
        if test_case.when.get('override_conditions'):
            # Replace all previous conditions
            conditions = [test_case.when]
        else:
            # Add to conditions (AND logic)
            conditions.append(test_case.when)
    
    # If no conditions, test runs
    if not conditions:
        return True, "No conditions specified"
    
    # Evaluate all conditions (AND logic)
    for condition in conditions:
        result, reason = evaluate_condition(condition, current_scope, env_vars)
        if not result:
            return False, reason
    
    return True, "All conditions met"


def evaluate_condition(condition, current_scope, env_vars):
    """Evaluate a single condition."""
    
    # Scope check
    if 'scope' in condition:
        if current_scope not in condition['scope']:
            return False, f"Scope {current_scope} not in {condition['scope']}"
    
    if 'not_scope' in condition:
        if current_scope in condition['not_scope']:
            return False, f"Scope {current_scope} in exclusion list"
    
    # Environment variable check
    if 'env' in condition:
        for key, expected in condition['env'].items():
            actual = env_vars.get(key)
            if expected == "*":
                if not actual:
                    return False, f"Env var {key} not set"
            elif actual != expected:
                return False, f"Env var {key}={actual}, expected {expected}"
    
    # Model availability check
    if 'models_available' in condition:
        # Check if required models are configured
        pass
    
    # Complex conditions
    if 'all' in condition:
        for sub_condition in condition['all']:
            result, reason = evaluate_condition(sub_condition, current_scope, env_vars)
            if not result:
                return False, reason
    
    if 'any' in condition:
        for sub_condition in condition['any']:
            result, reason = evaluate_condition(sub_condition, current_scope, env_vars)
            if result:
                return True, "At least one condition met"
        return False, "No conditions in 'any' were met"
    
    return True, "Condition met"


def resolve_config(test_case, container, global_config):
    """
    Resolve configuration for a test case.
    
    Args:
        test_case: TestCase object (inline or referenced)
        container: Prompt or TestSuite containing the test
        global_config: Global .grompt config
    
    Returns:
        Fully resolved configuration
    """
    
    # Start with system defaults
    config = {
        'eval_method': 'semantic',
        'eval_config': {},
        'weight': 1.0,
        'models': None,
        'when': None,
        'skip': False,
    }
    
    # Layer 1: Global defaults
    if 'eval' in global_config:
        default_method = global_config['eval'].get('default_method', 'semantic')
        config['eval_method'] = default_method
        
        method_defaults = global_config['eval'].get('methods', {}).get(default_method, {})
        config['eval_config'].update(method_defaults)
    
    # Layer 2: Container defaults (only for inline tests)
    if not test_case.is_reference:
        if container.eval_method:
            config['eval_method'] = container.eval_method
        if container.eval_config:
            config['eval_config'].update(container.eval_config)
        if container.when:
            config['when'] = container.when
    
    # Layer 3: Test case specification (highest priority)
    if test_case.eval_method:
        config['eval_method'] = test_case.eval_method
    if test_case.eval_config:
        config['eval_config'].update(test_case.eval_config)
    if test_case.weight is not None:
        config['weight'] = test_case.weight
    if test_case.models is not None:
        config['models'] = test_case.models
    if test_case.when is not None:
        if test_case.when.get('override_conditions'):
            config['when'] = test_case.when
        else:
            # Combine conditions
            config['when'] = combine_conditions(config.get('when'), test_case.when)
    if test_case.skip:
        config['skip'] = True
        config['skip_reason'] = test_case.skip_reason
    
    # Resolve custom evaluators
    if config['eval_method'] in global_config.get('evaluators', {}):
        evaluator_def = global_config['evaluators'][config['eval_method']]
        default_args = evaluator_def.get('default_args', {})
        merged_config = default_args.copy()
        merged_config.update(config['eval_config'])
        config['eval_config'] = merged_config
        config['evaluator_class'] = evaluator_def['class']
    
    return config


def combine_conditions(cond1, cond2):
    """Combine two conditions with AND logic."""
    if not cond1:
        return cond2
    if not cond2:
        return cond1
    
    return {
        'all': [cond1, cond2]
    }
```

---

## Configuration Schema

### Complete Canonical Schema with Conditions

```yaml
# ============================================
# SYSTEM LEVEL (.grompt)
# ============================================
version: 1

# Infrastructure
prompts_dir: prompts
tests_dir: tests
cache_dir: .grompt/cache

# Scope definitions (system-level only)
scopes:
  local:
    description: "Local development"
    default: true
  
  ci:
    description: "Continuous Integration"
    env:
      CI: "true"
  
  production:
    description: "Production validation"
    env:
      PRODUCTION: "true"
  
  quick:
    description: "Quick smoke tests"
    max_duration: 5

# Model definitions
models:
  gpt-4:
    provider: openai
    api_key_env: OPENAI_API_KEY

# Custom evaluators
evaluators:
  security_check:
    class: "my_package.SecurityEvaluator"
    default_args:
      strict_mode: true

# Global eval defaults
eval:
  default_method: semantic
  methods:
    semantic:
      model: gpt-4
      threshold: 0.8

# ============================================
# SHARED TEST DEFINITIONS (tests/common/*.yaml)
# ============================================
test_cases:
  - name: "division_by_zero"
    when:
      scope: ["ci", "production"]
    weight: 1.0
    eval_method: "semantic"
    input:
      code: "def calc(x,y): return x/y"
    expected_meaning:
      - "warns about division by zero"
  
  - name: "quick_smoke_test"
    when:
      scope: ["local", "quick"]
    eval_method: "regex"
    input: {...}

# ============================================
# PROMPT LEVEL (prompts/*.yaml)
# ============================================
id: code-review
version: 1
model: gpt-4

template: |
  Review this code:
  {{ code }}

# Prompt-level condition (applies to inline tests)
when:
  scope: ["ci", "production"]

# Prompt-level defaults
eval_method: semantic
eval_config:
  threshold: 0.85

test_cases:
  # Inline test - inherits prompt condition
  - name: "test1"
    input:
      code: "def add(a, b): return a + b"
    # Effective: when.scope=["ci", "production"]
  
  # Inline test - override condition
  - name: "test2"
    when:
      scope: ["local"]
      override_conditions: true
    input: {...}
    # Effective: when.scope=["local"]
  
  # Referenced test - combines conditions
  - ref: "tests/common/edge-cases.yaml#division_by_zero"
    # Reference has: when.scope=["ci", "production"]
    # Prompt has: when.scope=["ci", "production"]
    # Effective: when.scope=["ci", "production"] (intersection)
  
  # Referenced test - override weight
  - ref: "tests/common/edge-cases.yaml#division_by_zero"
    weight: 2.0
    when:
      scope: ["ci"]
      override_conditions: true
    # Effective: when.scope=["ci"], weight=2.0
  
  # Skipped test
  - name: "broken_test"
    skip: true
    skip_reason: "Known issue #123 - API endpoint changed"
    input: {...}

# ============================================
# TEST SUITE LEVEL (tests/suites/*.yaml)
# ============================================
name: comprehensive
description: "Comprehensive test suite"

# Suite-level condition
when:
  scope: ["ci"]

# Suite-level defaults
eval_method: api
eval_config:
  api_url: "https://example.com"

# Include other suites
includes:
  - "tests/suites/security.yaml"

test_cases:
  # Inline test - inherits suite condition
  - name: "suite_test"
    input: {...}
    # Effective: when.scope=["ci"]
  
  # Referenced test - combines conditions
  - ref: "tests/common/edge-cases.yaml#division_by_zero"
    # Reference: when.scope=["ci", "production"]
    # Suite: when.scope=["ci"]
    # Effective: when.scope=["ci"] (intersection)
  
  # Referenced test with additional condition
  - ref: "tests/common/edge-cases.yaml#quick_smoke_test"
    when:
      env:
        VERBOSE: "true"
    # Reference: when.scope=["local", "quick"]
    # Suite: when.scope=["ci"]
    # Additional: env.VERBOSE="true"
    # Effective: when.all=[scope=["ci"], scope=["local","quick"], env.VERBOSE="true"]
    # Result: Never runs (scope intersection is empty)
```

---

## Configuration Matrix

| Option | System | Shared | Prompt | Suite | Test | Inheritance | Combinable |
|--------|--------|--------|--------|-------|------|-------------|------------|
| `scopes` | ✓ | - | - | - | - | No | No |
| `when` | - | ✓ | ✓ | ✓ | ✓ | Inline only | Yes (AND) |
| `skip` | - | ✓ | - | - | ✓ | No | No |
| `eval_method` | Default | ✓ | ✓ | ✓ | ✓ | Inline only | No |
| `eval_config` | Default | ✓ | ✓ | ✓ | ✓ | Inline only | Yes (merge) |
| `weight` | - | ✓ | - | ✓ | ✓ | Always overridable | No |

**Condition Combination:**
- Multiple `when` conditions combine with AND logic
- Scopes are intersected
- Env requirements are unioned
- `override_conditions: true` replaces all previous conditions

---

## CLI Usage with Scopes

```bash
# Run tests in specific scope
$ grompt test code-review --scope ci

# Run tests in multiple scopes (OR logic)
$ grompt test code-review --scope ci --scope production

# Run with environment variables
$ FEATURE_X=true grompt test code-review --scope local

# List available scopes
$ grompt scopes list

# Show which tests would run in a scope
$ grompt test code-review --scope ci --dry-run

# Force run all tests (ignore conditions)
$ grompt test code-review --force-all

# Run only skipped tests (for debugging)
$ grompt test code-review --only-skipped
```

---

## Examples

### Example 1: Environment-Specific Tests

```yaml
# .grompt
scopes:
  local:
    description: "Local development"
    default: true
  ci:
    description: "CI pipeline"
  production:
    description: "Production validation"

# prompts/code-review.yaml
test_cases:
  # Quick test for local development
  - name: "quick_check"
    when:
      scope: ["local"]
    eval_method: "regex"
    input: {...}
  
  # Comprehensive test for CI
  - name: "full_analysis"
    when:
      scope: ["ci", "production"]
    eval_method: "api"
    input: {...}
  
  # Expensive test only for production
  - name: "security_audit"
    when:
      all:
        - scope: ["production"]
        - env:
            SECURITY_API_KEY: "*"
    eval_method: "custom"
    eval_config:
      evaluator_class: "SecurityAuditor"
```

### Example 2: Feature Flag Testing

```yaml
test_cases:
  # Test new feature only when enabled
  - name: "new_feature_test"
    when:
      env:
        FEATURE_NEW_PARSER: "true"
    input: {...}
  
  # Test old behavior when feature disabled
  - name: "legacy_behavior_test"
    when:
      env:
        FEATURE_NEW_PARSER: "false"
    input: {...}
```

### Example 3: Conditional Suite Inclusion

```yaml
# tests/suites/comprehensive.yaml
name: "comprehensive"

when:
  scope: ["ci"]

includes:
  - "tests/suites/quick.yaml"  # Always included
  - "tests/suites/security.yaml"  # Runs only in CI

test_cases:
  - name: "integration_test"
    when:
      all:
        - scope: ["ci"]
        - env:
            DATABASE_URL: "*"
```

### Example 4: Temporarily Disabled Tests

```yaml
test_cases:
  - name: "flaky_test"
    skip: true
    skip_reason: "Flaky due to external API - issue #456"
    input: {...}
  
  - name: "wip_test"
    skip: true
    skip_reason: "Work in progress - not ready for CI"
    input: {...}
```

### Example 5: Model Availability Conditions

```yaml
test_cases:
  - name: "gpt4_specific_test"
    when:
      models_available: ["gpt-4"]
    models: ["gpt-4"]
    input: {...}
  
  - name: "fallback_test"
    when:
      not:
        models_available: ["gpt-4"]
    models: ["gpt-3.5-turbo"]
    input: {...}
```

---

## Implementation

### Test Case Model with Conditions

```python
# grompt/core/test_case.py

from dataclasses import dataclass
from typing import Dict, List, Optional, Union

@dataclass
class Condition:
    """Represents a test execution condition."""
    scope: List[str] = None
    not_scope: List[str] = None
    env: Dict[str, str] = None
    models_available: List[str] = None
    all: List['Condition'] = None
    any: List['Condition'] = None
    override_conditions: bool = False
    
    @classmethod
    def from_dict(cls, data: Dict) -> "Condition":
        if not data:
            return None
        return cls(
            scope=data.get('scope'),
            not_scope=data.get('not_scope'),
            env=data.get('env'),
            models_available=data.get('models_available'),
            all=[cls.from_dict(c) for c in data.get('all', [])],
            any=[cls.from_dict(c) for c in data.get('any', [])],
            override_conditions=data.get('override_conditions', False),
        )

@dataclass
class TestCase:
    name: str
    weight: float = 1.0
    models: List[str] = None
    input: Dict = None
    expected_meaning: Union[List[str], Dict] = None
    expected_score: Dict = None
    eval_method: str = None
    eval_config: Dict = None
    when: Condition = None
    skip: bool = False
    skip_reason: str = None
    
    # Reference tracking
    is_reference: bool = False
    reference_source: str = None
    
    @classmethod
    def from_dict(cls, data: Dict, is_reference: bool = False) -> "TestCase":
        return cls(
            name=data["name"],
            weight=data.get("weight", 1.0),
            models=data.get("models"),
            input=data.get("input"),
            expected_meaning=data.get("expected_meaning"),
            expected_score=data.get("expected_score"),
            eval_method=data.get("eval_method"),
            eval_config=data.get("eval_config"),
            when=Condition.from_dict(data.get("when")),
            skip=data.get("skip", False),
            skip_reason=data.get("skip_reason"),
            is_reference=is_reference,
        )

@dataclass
class TestSuite:
    name: str
    description: str = ""
    weight: float = 1.0
    test_cases: List[Union[TestCase, Dict]] = None
    includes: List[str] = None
    eval_method: str = None
    eval_config: Dict = None
    when: Condition = None
```

### Condition Evaluator

```python
# grompt/core/condition_evaluator.py

import os
from typing import Dict, Tuple

class ConditionEvaluator:
    """Evaluate test execution conditions."""
    
    def __init__(self, current_scope: str, env_vars: Dict[str, str] = None):
        self.current_scope = current_scope
        self.env_vars = env_vars or os.environ.copy()
    
    def should_run(self, test_case: TestCase, container=None) -> Tuple[bool, str]:
        """Determine if test should run."""
        
        # Check explicit skip
        if test_case.skip:
            return False, test_case.skip_reason or "Explicitly skipped"
        
        # Collect conditions
        conditions = []
        
        # Container condition (for inline tests)
        if not test_case.is_reference and container and container.when:
            conditions.append(container.when)
        
        # Test condition
        if test_case.when:
            if test_case.when.override_conditions:
                conditions = [test_case.when]
            else:
                conditions.append(test_case.when)
        
        # If no conditions, test runs
        if not conditions:
            return True, "No conditions specified"
        
        # Evaluate all conditions (AND logic)
        for condition in conditions:
            result, reason = self.evaluate(condition)
            if not result:
                return False, reason
        
        return True, "All conditions met"
    
    def evaluate(self, condition: Condition) -> Tuple[bool, str]:
        """Evaluate a single condition."""
        
        if not condition:
            return True, "No condition"
        
        # Scope check
        if condition.scope:
            if self.current_scope not in condition.scope:
                return False, f"Scope '{self.current_scope}' not in {condition.scope}"
        
        if condition.not_scope:
            if self.current_scope in condition.not_scope:
                return False, f"Scope '{self.current_scope}' in exclusion list {condition.not_scope}"
        
        # Environment variable check
        if condition.env:
            for key, expected in condition.env.items():
                actual = self.env_vars.get(key)
                if expected == "*":
                    if not actual:
                        return False, f"Environment variable '{key}' not set"
                elif actual != expected:
                    return False, f"Environment variable '{key}'='{actual}', expected '{expected}'"
        
        # Model availability check
        if condition.models_available:
            # Would check against configured models
            pass
        
        # Complex conditions
        if condition.all:
            for sub_condition in condition.all:
                result, reason = self.evaluate(sub_condition)
                if not result:
                    return False, f"AND condition failed: {reason}"
        
        if condition.any:
            any_met = False
            for sub_condition in condition.any:
                result, reason = self.evaluate(sub_condition)
                if result:
                    any_met = True
                    break
            if not any_met:
                return False, "No OR conditions were met"
        
        return True, "Condition met"
```

---

## Best Practices

### 1. Use Scopes for Environment Separation

```yaml
# Good: Clear scope-based separation
test_cases:
  - name: "quick_smoke_test"
    when:
      scope: ["local", "quick"]
    eval_method: "regex"
  
  - name: "comprehensive_test"
    when:
      scope: ["ci", "production"]
    eval_method: "api"
```

### 2. Document Skip Reasons

```yaml
# Good: Clear reason for skipping
test_cases:
  - name: "flaky_test"
    skip: true
    skip_reason: "Flaky due to external API timeout - issue #456"
  
# Bad: No explanation
test_cases:
  - name: "test1"
    skip: true
```

### 3. Use Feature Flags for Gradual Rollout

```yaml
# Good: Test both old and new behavior
test_cases:
  - name: "new_parser_test"
    when:
      env:
        FEATURE_NEW_PARSER: "true"
    input: {...}
  
  - name: "legacy_parser_test"
    when:
      env:
        FEATURE_NEW_PARSER: "false"
    input: {...}
```

### 4. Combine Conditions Explicitly

```yaml
# Good: Clear intent with 'all'
test_cases:
  - name: "production_security_test"
    when:
      all:
        - scope: ["production"]
        - env:
            SECURITY_API_KEY: "*"
    input: {...}

# Avoid: Implicit combination can be confusing
```

### 5. Use override_conditions Sparingly

```yaml
# Good: Only override when truly needed
test_cases:
  - ref: "tests/common/security.yaml#sql_injection"
    when:
      scope: ["local"]  # Run locally for debugging
      override_conditions: true
    
# Better: Create a new test case if behavior differs significantly
```

---

## Summary

### The Canonical Set with Conditions

1. **System Level** (`.grompt`): Infrastructure, models, custom evaluators, **scope definitions**
2. **Shared Definitions** (`tests/common/*.yaml`): Reusable test templates **with conditions**
3. **Container Level** (prompts/suites): Defaults for inline tests, **container-level conditions**
4. **Test Level**: Final specification (inline or referenced), **test-level conditions**

### Key Principles

1. **Referenced tests preserve their conditions** - They work the same everywhere
2. **Inline tests inherit container conditions** - Convenient for common patterns
3. **Conditions combine with AND logic** - Multiple conditions must all be met
4. **Skip takes precedence** - Skipped tests never run, regardless of conditions
5. **Explicit override available** - Use `override_conditions: true` when needed
6. **Scopes are defined globally** - Ensures consistency across all tests

### Condition Resolution Order

```
Test skip flag (highest - always honored)
  ↓
Test condition (with override_conditions)
  ↓
Container condition (for inline tests)
  ↓
Reference condition (for referenced tests)
  ↓
No conditions (test runs)
```

### Condition Combination Rules

When multiple conditions apply:
- **Scopes**: Intersection (test must be in ALL specified scopes)
- **Environment variables**: Union (ALL env requirements must be met)
- **Complex conditions**: Evaluated according to `all`/`any` logic
- **Override**: `override_conditions: true` replaces all previous conditions

### CLI Scope Usage

```bash
# Run in specific scope
$ grompt test code-review --scope ci

# Show what would run
$ grompt test code-review --scope ci --dry-run

# Force run all (ignore conditions)
$ grompt test code-review --force-all

# List available scopes
$ grompt scopes list
```

This canonical set provides a **predictable, composable, extensible, and conditional** configuration system that supports:
- ✅ Test case composition and reuse
- ✅ Custom evaluator functions
- ✅ Conditional execution based on scopes and environment
- ✅ Clear override and inheritance rules
- ✅ Flexible condition combinations
- ✅ Explicit skip mechanism with documentation

The system is designed to scale from simple local development workflows to complex CI/CD pipelines with multiple environments and testing strategies!
                