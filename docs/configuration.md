# Configuration

## Global Config (.grompt)

```yaml
version: 1
prompts_dir: prompts
tests_dir: tests
default_model: gpt-4

# Model configurations
models:
  gpt-4:
    provider: openai
    api_key_env: OPENAI_API_KEY
    max_tokens: 8192
  
  gpt-3.5-turbo:
    provider: openai
    api_key_env: OPENAI_API_KEY
    max_tokens: 4096
  
  claude-3-opus:
    provider: anthropic
    api_key_env: ANTHROPIC_API_KEY
    max_tokens: 200000

# Model groups
model_groups:
  openai: ["gpt-4", "gpt-3.5-turbo"]
  anthropic: ["claude-3-opus", "claude-3-sonnet"]
  all: ["gpt-4", "gpt-3.5-turbo", "claude-3-opus"]
```

