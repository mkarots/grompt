# Best Practices

## 1. Document Variables

Always document expected variables:

```yaml
variables:
  code:
    type: string
    required: true
    description: "Code to review"
  language:
    type: string
    required: false
    default: "Python"
    description: "Programming language of the code"
```

## 2. Provide Test Cases

Include test cases with realistic data:

```yaml
test_cases:
  - name: "realistic_example"
    input:
      code: |
        # Real code example
        def process_payment(amount, currency="USD"):
            if amount <= 0:
                raise ValueError("Amount must be positive")
            return {"amount": amount, "currency": currency}
    expected_meaning:
      - "validates input"
      - "handles currency"
```

## 3. Use Defaults Wisely

Provide sensible defaults for optional variables:

```yaml
variables:
  max_length:
    type: integer
    required: false
    default: 100
    description: "Maximum response length"
```

## 4. Version Incrementally

Commit changes with clear messages:

```bash
grompt commit code-review "Added language parameter for multi-language support"
```

## 5. Test Before Deploying

Always test prompts with real data before using in production:

```bash
grompt test code-review --var code="$(cat production_example.py)"
```

