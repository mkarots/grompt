# Variable Validation

## Defining Variable Schema

```yaml
# prompts/api-call.yaml
id: api-call
version: 1
model: gpt-4

variables:
  endpoint:
    type: string
    required: true
    pattern: "^/api/.*"
    description: API endpoint path
  
  method:
    type: string
    required: true
    enum: ["GET", "POST", "PUT", "DELETE"]
    description: HTTP method
  
  params:
    type: object
    required: false
    description: Query parameters
  
  max_retries:
    type: integer
    required: false
    default: 3
    min: 1
    max: 10
    description: Maximum retry attempts

template: |
  Generate a {{ method }} request to {{ endpoint }}
  {% if params %}
  with parameters: {{ params }}
  {% endif %}
  
  Max retries: {{ max_retries }}
```

## Validating Variables

```bash
# Validate prompt definition
grompt validate api-call

# Test with validation
grompt test api-call \
  --var endpoint="/api/users" \
  --var method="GET" \
  --var params='{"limit": 10}'
```

