# Grompt Test Case System

## Overview

A flexible test case system that allows you to:
- Define individual test cases with expected meanings
- Weight test cases by importance
- Compose test cases into named suites
- Use different evaluation methods per test case or suite

---

## Test Case Structure

### 1. Individual Test Case

```yaml
# prompts/code-review.yaml
id: code-review
version: 1
model: gpt-4
template: |
  Review this code:
  {{ code }}

# Individual test cases
test_cases:
  - name: "simple_function"
    weight: 1.0
    models: ["gpt-4", "gpt-3.5-turbo"]  # Run against these models
    input:
      code: "def add(a, b): return a + b"
    expected_meaning:
      - "mentions code quality"
      - "identifies simple function"
      - "no critical issues"
    eval_method: "semantic"
  
  - name: "division_bug"
    weight: 2.0
    models: ["gpt-4", "claude-3-opus"]  # Test with specific models
    input:
      code: "def calc(x,y): return x/y"
    expected_meaning:
      - "warns about division by zero"
      - "suggests error handling"
    eval_method: "api"
    eval_config:
      api_url: "https://eval.example.com/v1/check"
  
  - name: "all_models_test"
    weight: 1.0
    models: "*"  # Run against all configured models
    input:
      code: "def process(data): return data.value"
    expected_meaning:
      - "warns about potential null/None"
```

### 2. Test Suites (Composable Groups)

```yaml
# tests/code-review-suite.yaml
name: "code-review-comprehensive"
description: "Comprehensive test suite for code review prompts"

# Reference test cases from different sources
test_cases:
  # Inline test case
  - name: "simple_function"
    weight: 1.0
    input:
      code: "def add(a, b): return a + b"
    expected_meaning:
      - "mentions code quality"
  
  # Reference test case from another file
  - ref: "tests/common/edge-cases.yaml#division_by_zero"
    weight: 2.0
  
  # Reference test case from prompt file
  - ref: "prompts/code-review.yaml#test_cases[0]"
    weight: 1.5

# Suite-level eval method (can be overridden per test)
eval_method: "semantic"
eval_config:
  model: "gpt-4"
  threshold: 0.8
```

### 3. Shared Test Cases

```yaml
# tests/common/edge-cases.yaml
# Reusable test cases that can be referenced

test_cases:
  - name: "division_by_zero"
    input:
      code: "def calc(x,y): return x/y"
    expected_meaning:
      - "warns about division by zero"
      - "suggests error handling"
  
  - name: "null_pointer"
    input:
      code: "def process(data): return data.value"
    expected_meaning:
      - "warns about potential null/None"
      - "suggests null checking"
  
  - name: "sql_injection"
    input:
      code: "query = f'SELECT * FROM users WHERE id={user_id}'"
    expected_meaning:
      - "identifies SQL injection risk"
      - "suggests parameterized queries"
```

---

## Evaluation Methods

### 1. Semantic Matching (Default)

```yaml
test_cases:
  - name: "test1"
    eval_method: "semantic"
    eval_config:
      model: "gpt-4"  # LLM to use for semantic comparison
      threshold: 0.8  # Minimum similarity score
    input:
      code: "def add(a, b): return a + b"
    expected_meaning:
      - "mentions code quality"
      - "identifies simple function"
```

**How it works:**
- Renders prompt with test input
- Checks if output semantically contains expected meanings
- Uses LLM to judge semantic similarity

### 2. API-Based Evaluation

```yaml
test_cases:
  - name: "test1"
    eval_method: "api"
    eval_config:
      api_url: "https://eval.example.com/v1/evaluate"
      api_key_env: "EVAL_API_KEY"
      request_template:
        prompt: "{{ rendered_prompt }}"
        expected: "{{ expected_meaning }}"
      response_path: "result.score"  # JSONPath to score
    input:
      code: "def add(a, b): return a + b"
    expected_meaning:
      - "mentions code quality"
```

**API Request:**
```json
POST https://eval.example.com/v1/evaluate
{
  "prompt": "Review this code:\n\ndef add(a, b): return a + b",
  "expected": ["mentions code quality", "identifies simple function"]
}
```

**API Response:**
```json
{
  "result": {
    "score": 0.92,
    "matches": [
      {"meaning": "mentions code quality", "found": true, "confidence": 0.95},
      {"meaning": "identifies simple function", "found": true, "confidence": 0.89}
    ]
  }
}
```

### 3. Criteria-Based Evaluation

```yaml
test_cases:
  - name: "test1"
    eval_method: "criteria"
    eval_config:
      criteria:
        - name: "clarity"
          weight: 0.3
        - name: "completeness"
          weight: 0.7
    input:
      code: "def add(a, b): return a + b"
    expected_score:
      min_total: 0.8
      min_clarity: 0.7
      min_completeness: 0.8
```

### 4. Regex Matching

```yaml
test_cases:
  - name: "test1"
    eval_method: "regex"
    eval_config:
      patterns:
        - pattern: "code quality"
          required: true
        - pattern: "simple function"
          required: true
        - pattern: "bug|issue|problem"
          required: false
    input:
      code: "def add(a, b): return a + b"
```

### 5. Custom Evaluator

```yaml
test_cases:
  - name: "test1"
    eval_method: "custom"
    eval_config:
      evaluator_class: "my_package.MyEvaluator"
      evaluator_args:
        threshold: 0.8
    input:
      code: "def add(a, b): return a + b"
    expected_meaning:
      - "mentions code quality"
```

---

## Weighted Test Cases

### Simple Weighting

```yaml
test_cases:
  - name: "critical_bug"
    weight: 3.0  # 3x more important
    input:
      code: "def calc(x,y): return x/y"
    expected_meaning:
      - "warns about division by zero"
  
  - name: "style_issue"
    weight: 1.0  # Normal importance
    input:
      code: "def add(a,b):return a+b"
    expected_meaning:
      - "mentions spacing"
  
  - name: "minor_suggestion"
    weight: 0.5  # Less important
    input:
      code: "def add(a, b): return a + b"
    expected_meaning:
      - "suggests type hints"
```

**Score Calculation:**
```python
total_score = sum(test.score * test.weight for test in tests) / sum(test.weight for test in tests)
```

### Category Weighting

```yaml
test_suites:
  - name: "security"
    weight: 3.0
    test_cases:
      - name: "sql_injection"
        weight: 1.0
      - name: "xss"
        weight: 1.0
  
  - name: "style"
    weight: 1.0
    test_cases:
      - name: "spacing"
        weight: 1.0
      - name: "naming"
        weight: 1.0
```

---

## Composable Test Suites

### Suite Definition

```yaml
# tests/suites/comprehensive.yaml
name: "comprehensive-code-review"
description: "Full test suite for code review"

# Include other suites
includes:
  - "tests/suites/security.yaml"
  - "tests/suites/performance.yaml"
  - "tests/suites/style.yaml"

# Add suite-specific tests
test_cases:
  - name: "integration_test"
    weight: 2.0
    input:
      code: |
        def process_user(user_id):
            query = f"SELECT * FROM users WHERE id={user_id}"
            result = db.execute(query)
            return result.value
    expected_meaning:
      - "identifies SQL injection"
      - "warns about null pointer"
      - "suggests error handling"

# Suite-level configuration
eval_method: "api"
eval_config:
  api_url: "https://eval.example.com/v1/evaluate"
```

### Security Suite

```yaml
# tests/suites/security.yaml
name: "security"
weight: 3.0

test_cases:
  - ref: "tests/common/edge-cases.yaml#sql_injection"
    weight: 2.0
  
  - ref: "tests/common/edge-cases.yaml#xss"
    weight: 2.0
  
  - name: "path_traversal"
    weight: 1.5
    input:
      code: "open(user_input, 'r')"
    expected_meaning:
      - "warns about path traversal"
```

### Using Suites

```bash
# Run specific suite
$ grompt test code-review --suite comprehensive

# Run multiple suites
$ grompt test code-review --suite security --suite performance

# Run all suites
$ grompt test code-review --all-suites
```

---

## Configuration Examples

### Prompt with Multiple Eval Methods

```yaml
# prompts/code-review.yaml
id: code-review
version: 1
model: gpt-4
template: |
  Review this code:
  {{ code }}

# Default eval method for all tests
eval_method: "semantic"
eval_config:
  model: "gpt-4"
  threshold: 0.8

test_cases:
  # Uses default semantic eval
  - name: "simple_function"
    weight: 1.0
    input:
      code: "def add(a, b): return a + b"
    expected_meaning:
      - "mentions code quality"
  
  # Override with API eval
  - name: "security_check"
    weight: 2.0
    eval_method: "api"
    eval_config:
      api_url: "https://security-eval.example.com/v1/check"
    input:
      code: "query = f'SELECT * FROM users WHERE id={user_id}'"
    expected_meaning:
      - "identifies SQL injection"
  
  # Override with criteria eval
  - name: "performance_check"
    weight: 1.5
    eval_method: "criteria"
    eval_config:
      criteria:
        - name: "efficiency"
          weight: 1.0
    input:
      code: "for i in range(len(arr)): print(arr[i])"
    expected_score:
      min_efficiency: 0.7
```

### Global Eval Configuration

```yaml
# .grompt
version: 1
prompts_dir: prompts
default_model: gpt-4

# Global eval configuration
eval:
  # Default eval method
  default_method: "semantic"
  
  # Eval method configurations
  methods:
    semantic:
      model: "gpt-4"
      threshold: 0.8
    
    api:
      api_url: "https://eval.example.com/v1/evaluate"
      api_key_env: "EVAL_API_KEY"
      timeout: 30
    
    criteria:
      default_criteria:
        - name: "clarity"
          weight: 0.3
        - name: "completeness"
          weight: 0.7
  
  # Test suite directories
  suite_dirs:
    - "tests/suites"
    - "tests/common"
```

---

## Implementation

### Test Case Model

```python
# grompt/core/test_case.py

from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class TestCase:
    name: str
    weight: float = 1.0
    input: Dict = None
    expected_meaning: List[str] = None
    expected_score: Dict = None
    eval_method: str = "semantic"
    eval_config: Dict = None
    
    @classmethod
    def from_dict(cls, data: Dict) -> "TestCase":
        return cls(
            name=data["name"],
            weight=data.get("weight", 1.0),
            input=data.get("input", {}),
            expected_meaning=data.get("expected_meaning", []),
            expected_score=data.get("expected_score", {}),
            eval_method=data.get("eval_method", "semantic"),
            eval_config=data.get("eval_config", {}),
        )

@dataclass
class TestSuite:
    name: str
    description: str = ""
    weight: float = 1.0
    test_cases: List[TestCase] = None
    includes: List[str] = None
    eval_method: str = "semantic"
    eval_config: Dict = None
    
    def resolve_includes(self, loader):
        """Resolve included suites and test case references."""
        all_tests = []
        
        # Load included suites
        for include_path in self.includes or []:
            suite = loader.load_suite(include_path)
            all_tests.extend(suite.test_cases)
        
        # Add own test cases
        for test in self.test_cases or []:
            if isinstance(test, dict) and "ref" in test:
                # Resolve reference
                referenced_test = loader.load_test_ref(test["ref"])
                referenced_test.weight = test.get("weight", referenced_test.weight)
                all_tests.append(referenced_test)
            else:
                all_tests.append(test)
        
        return all_tests
```

### Evaluator Registry

```python
# grompt/core/evaluator_registry.py

class EvaluatorRegistry:
    _evaluators = {}
    
    @classmethod
    def register(cls, name: str, evaluator_class):
        cls._evaluators[name] = evaluator_class
    
    @classmethod
    def get(cls, name: str):
        return cls._evaluators.get(name)

# Register built-in evaluators
EvaluatorRegistry.register("semantic", SemanticEvaluator)
EvaluatorRegistry.register("api", APIEvaluator)
EvaluatorRegistry.register("criteria", CriteriaEvaluator)
EvaluatorRegistry.register("regex", RegexEvaluator)
```

### Test Runner

```python
# grompt/application/test_runner.py

class TestRunner:
    def run_test_case(self, prompt: Prompt, test_case: TestCase) -> Dict:
        # Get evaluator
        evaluator_class = EvaluatorRegistry.get(test_case.eval_method)
        evaluator = evaluator_class(test_case.eval_config)
        
        # Render prompt with test input
        rendered = TemplateRenderer.render(prompt.template, **test_case.input)
        
        # Evaluate
        result = evaluator.evaluate(rendered, test_case)
        
        return {
            "test_case": test_case.name,
            "score": result["score"],
            "weight": test_case.weight,
            "weighted_score": result["score"] * test_case.weight,
            "details": result.get("details", {}),
        }
    
    def run_suite(self, prompt: Prompt, suite: TestSuite) -> Dict:
        results = []
        total_weight = 0
        weighted_sum = 0
        
        for test_case in suite.test_cases:
            result = self.run_test_case(prompt, test_case)
            results.append(result)
            total_weight += test_case.weight
            weighted_sum += result["weighted_score"]
        
        return {
            "suite": suite.name,
            "total_score": weighted_sum / total_weight if total_weight > 0 else 0,
            "results": results,
        }
```

---

## CLI Usage

```bash
# Run tests from prompt file
$ grompt test code-review

# Run specific suite
$ grompt test code-review --suite comprehensive

# Run with specific eval method
$ grompt test code-review --eval-method api


---

## Model-Specific Testing

### Specify Models Per Test Case

```yaml
test_cases:
  # Test against specific models
  - name: "gpt4_specific"
    models: ["gpt-4", "gpt-4-turbo"]
    input:
      code: "def add(a, b): return a + b"
    expected_meaning:
      - "mentions code quality"
  
  # Test against all models
  - name: "cross_model_test"
    models: "*"
    input:
      code: "def calc(x,y): return x/y"
    expected_meaning:
      - "warns about division by zero"
  
  # Test against Claude models only
  - name: "claude_specific"
    models: ["claude-3-opus", "claude-3-sonnet"]
    input:
      code: "complex code here"
    expected_meaning:
      - "provides detailed analysis"
```

### Model-Specific Expected Results

```yaml
test_cases:
  - name: "model_aware_test"
    models: ["gpt-4", "claude-3-opus", "gpt-3.5-turbo"]
    input:
      code: "def process(data): return data.value"
    
    # Different expectations per model
    expected_meaning:
      default:
        - "warns about potential null/None"
      
      gpt-4:
        - "warns about potential null/None"
        - "suggests defensive programming"
        - "mentions type hints"
      
      claude-3-opus:
        - "warns about potential null/None"
        - "provides detailed error handling examples"
      
      gpt-3.5-turbo:
        - "warns about potential null/None"
```

### Model Configuration

```yaml
# .grompt
version: 1
prompts_dir: prompts
default_model: gpt-4

# Define available models for testing
models:
  gpt-4:
    provider: openai
    api_key_env: OPENAI_API_KEY
    max_tokens: 8192
  
  gpt-4-turbo:
    provider: openai
    api_key_env: OPENAI_API_KEY
    max_tokens: 128000
  
  gpt-3.5-turbo:
    provider: openai
    api_key_env: OPENAI_API_KEY
    max_tokens: 4096
  
  claude-3-opus:
    provider: anthropic
    api_key_env: ANTHROPIC_API_KEY
    max_tokens: 200000
  
  claude-3-sonnet:
    provider: anthropic
    api_key_env: ANTHROPIC_API_KEY
    max_tokens: 200000

# Model groups for easy reference
model_groups:
  openai: ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"]
  anthropic: ["claude-3-opus", "claude-3-sonnet"]
  all: ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo", "claude-3-opus", "claude-3-sonnet"]
```

### Using Model Groups

```yaml
test_cases:
  # Test against all OpenAI models
  - name: "openai_test"
    models: "@openai"  # Reference model group
    input:
      code: "def add(a, b): return a + b"
    expected_meaning:
      - "mentions code quality"
  
  # Test against all Anthropic models
  - name: "anthropic_test"
    models: "@anthropic"
    input:
      code: "complex code"
    expected_meaning:
      - "provides detailed analysis"
  
  # Test against all configured models
  - name: "universal_test"
    models: "@all"
    input:
      code: "def calc(x,y): return x/y"
    expected_meaning:
      - "warns about division by zero"
```

### CLI Usage with Models

```bash
# Run tests against specific models
$ grompt test code-review --models gpt-4,claude-3-opus

# Run tests against model group
$ grompt test code-review --models @openai

# Run tests against all models
$ grompt test code-review --models @all

# Override test case models
$ grompt test code-review --force-models gpt-4
```

### Test Results by Model

```
┌─ Test Results: code-review ────────────────────────────────────────┐
│                                                                     │
│ Test: simple_function                                              │
│ ├─ gpt-4           Score: 0.92  ✓                                  │
│ ├─ gpt-3.5-turbo   Score: 0.85  ✓                                  │
│ └─ claude-3-opus   Score: 0.95  ✓                                  │
│                                                                     │
│ Test: division_bug                                                 │
│ ├─ gpt-4           Score: 0.88  ✓                                  │
│ ├─ gpt-3.5-turbo   Score: 0.72  ✗ (below threshold)                │
│ └─ claude-3-opus   Score: 0.91  ✓                                  │
│                                                                     │
│ Overall Scores:                                                    │
│ ├─ gpt-4:          0.90  ✓                                         │
│ ├─ gpt-3.5-turbo:  0.79  ⚠                                         │
│ └─ claude-3-opus:  0.93  ✓                                         │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Implementation

```python
# grompt/core/test_case.py

@dataclass
class TestCase:
    name: str
    weight: float = 1.0
    models: List[str] = None  # ["gpt-4", "claude-3-opus"] or "*" or "@group"
    input: Dict = None
    expected_meaning: Dict = None  # Can be dict with model-specific expectations
    eval_method: str = "semantic"
    eval_config: Dict = None
    
    def get_models(self, config) -> List[str]:
        """Resolve model list from config."""
        if not self.models or self.models == "*":
            # Use all configured models
            return list(config.get("models", {}).keys())
        
        resolved_models = []
        for model in self.models:
            if model.startswith("@"):
                # Model group reference
                group_name = model[1:]
                group = config.get("model_groups", {}).get(group_name, [])
                resolved_models.extend(group)
            else:
                # Direct model name
                resolved_models.append(model)
        
        return resolved_models
    
    def get_expected_meaning(self, model: str) -> List[str]:
        """Get expected meaning for a specific model."""
        if isinstance(self.expected_meaning, list):
            # Same expectations for all models
            return self.expected_meaning
        
        # Model-specific expectations
        return self.expected_meaning.get(
            model,
            self.expected_meaning.get("default", [])
        )

# grompt/application/test_runner.py

class TestRunner:
    def run_test_case(self, prompt: Prompt, test_case: TestCase, model: str) -> Dict:
        # Get model-specific expectations
        expected = test_case.get_expected_meaning(model)
        
        # Get evaluator
        evaluator_class = EvaluatorRegistry.get(test_case.eval_method)
        evaluator = evaluator_class(test_case.eval_config)
        
        # Render prompt with test input using specified model
        rendered = TemplateRenderer.render(prompt.template, **test_case.input)
        
        # Evaluate
        result = evaluator.evaluate(rendered, expected, model=model)
        
        return {
            "test_case": test_case.name,
            "model": model,
            "score": result["score"],
            "weight": test_case.weight,
            "weighted_score": result["score"] * test_case.weight,
            "details": result.get("details", {}),
        }
    
    def run_test_case_all_models(self, prompt: Prompt, test_case: TestCase, config: Dict) -> List[Dict]:
        """Run a test case against all specified models."""
        models = test_case.get_models(config)
        results = []
        
        for model in models:
            result = self.run_test_case(prompt, test_case, model)
            results.append(result)
        
        return results
```

### Benefits of Model-Specific Testing

1. **Cross-Model Validation**: Ensure prompts work well across different LLMs
2. **Model Comparison**: Compare how different models handle the same prompt
3. **Targeted Testing**: Test specific models for specific use cases
4. **Flexible Expectations**: Different models may have different strengths
5. **Cost Optimization**: Test with cheaper models first, then expensive ones

# Show detailed results
$ grompt test code-review --verbose

# Run and save results
$ grompt test code-review --output results.json
```

---

## Benefits

1. **Flexible**: Multiple eval methods per test
2. **Composable**: Build complex suites from simple tests
3. **Weighted**: Prioritize important tests
4. **Reusable**: Share test cases across prompts
5. **Extensible**: Add custom evaluators
6. **Organized**: Group tests into suites

This system gives you complete control over how prompts are tested and evaluated!