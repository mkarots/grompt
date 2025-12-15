# CLI Commands

## Initialization

```bash
# Initialize grompt in current directory
grompt init

# Initialize with custom config
grompt init --prompts-dir my-prompts --model gpt-4
```

## Creating Prompts

```bash
# Create basic prompt
grompt add summarize

# Create with template
grompt add code-review --template "Review: {{ code }}"

# Create with options
grompt add translate \
  --model gpt-3.5-turbo \
  --description "Translates text between languages"

# Create in subdirectory
grompt add backend/api-prompt --dir backend
```

## Testing Prompts

```bash
# Test with single variable
grompt test summarize --var text="Long article..."

# Test with multiple variables
grompt test code-review \
  --var code="def hello(): pass" \
  --var language="Python"

# Test with file content
grompt test code-review --var code="$(cat src/main.py)"

# Run all test cases
grompt test code-review

# Run specific test case
grompt test code-review --case simple_function

# Test with different model
grompt test code-review --model gpt-3.5-turbo
```

## Validation

```bash
# Validate single prompt
grompt validate code-review

# Validate all prompts
grompt validate --all

# Check for missing variables
grompt validate code-review --check-vars
```

## Version Management

```bash
# Commit changes (increments version)
grompt commit code-review "Improved clarity"

# Show version history
grompt log code-review

# Compare versions
grompt diff code-review --from v1 --to v2
```

