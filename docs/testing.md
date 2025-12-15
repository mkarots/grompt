# Testing Prompts with Data

## Inline Test Cases

Define test cases directly in your prompt file:

```yaml
# prompts/code-review.yaml
id: code-review
version: 1
model: gpt-4
template: |
  Review this code:
  {{ code }}

# Test cases with real data
test_cases:
  - name: "simple_function"
    input:
      code: "def add(a, b): return a + b"
    expected_meaning:
      - "mentions code quality"
      - "identifies simple function"
      - "no critical issues"
  
  - name: "division_bug"
    input:
      code: "def calc(x,y): return x/y"
    expected_meaning:
      - "warns about division by zero"
      - "suggests error handling"
  
  - name: "complex_class"
    input:
      code: |
        class Calculator:
            def __init__(self):
                self.history = []
            
            def add(self, a, b):
                result = a + b
                self.history.append(result)
                return result
    expected_meaning:
      - "mentions class structure"
      - "notes history tracking"
```

## Separate Test Files

For larger test suites, use separate files:

```yaml
# tests/code-review-tests.yaml
prompt: code-review

test_cases:
  - name: "sql_injection"
    input:
      code: "query = f'SELECT * FROM users WHERE id={user_id}'"
    expected_meaning:
      - "identifies SQL injection risk"
      - "suggests parameterized queries"
  
  - name: "performance_issue"
    input:
      code: |
        for i in range(len(items)):
            print(items[i])
    expected_meaning:
      - "suggests enumerate or direct iteration"
      - "mentions performance"
```

## Running Tests

```bash
# Run tests defined in prompt file
grompt test code-review

# Run tests from separate file
grompt test code-review --test-file tests/code-review-tests.yaml

# Run specific test case
grompt test code-review --case simple_function

# Show detailed output
grompt test code-review --verbose
```

## Test with Multiple Models

```yaml
# prompts/code-review.yaml
test_cases:
  - name: "cross_model_test"
    models: ["gpt-4", "gpt-3.5-turbo", "claude-3-opus"]
    input:
      code: "def calc(x,y): return x/y"
    expected_meaning:
      - "warns about division by zero"
```

```bash
# Test against specific models
grompt test code-review --models gpt-4,claude-3-opus

# Test against all configured models
grompt test code-review --models @all
```

## Weighted Test Cases

Prioritize important tests:

```yaml
test_cases:
  - name: "critical_security"
    weight: 3.0  # 3x more important
    input:
      code: "eval(user_input)"
    expected_meaning:
      - "warns about code injection"
  
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

