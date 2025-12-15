# Real-World Examples

## Example 1: Code Review with Context

```yaml
# prompts/code-review-contextual.yaml
id: code-review-contextual
version: 1
model: gpt-4

variables:
  code:
    type: string
    required: true
  file_path:
    type: string
    required: true
  language:
    type: string
    required: false
    default: "Python"
  project_context:
    type: string
    required: false
    description: "Brief description of the project"

template: |
  You are reviewing code from a {{ language }} project.
  
  {% if project_context %}
  Project context: {{ project_context }}
  {% endif %}
  
  File: {{ file_path }}
  
  Code:
  ```{{ language.lower() }}
  {{ code }}
  ```
  
  Provide a detailed review covering:
  1. Code quality and readability
  2. Potential bugs or edge cases
  3. Performance considerations
  4. Security issues
  5. Best practices for {{ language }}

test_cases:
  - name: "with_context"
    input:
      code: "def process_payment(amount): return amount * 1.1"
      file_path: "src/payments/processor.py"
      language: "Python"
      project_context: "E-commerce payment processing system"
    expected_meaning:
      - "mentions payment processing"
      - "suggests validation"
      - "considers security"
```

## Example 2: Data Transformation

```yaml
# prompts/transform-data.yaml
id: transform-data
version: 1
model: gpt-4

variables:
  input_format:
    type: string
    required: true
    enum: ["JSON", "CSV", "XML"]
  output_format:
    type: string
    required: true
    enum: ["JSON", "CSV", "XML"]
  data:
    type: string
    required: true
  schema:
    type: object
    required: false

template: |
  Convert this {{ input_format }} data to {{ output_format }}:
  
  Input:
  {{ data }}
  
  {% if schema %}
  Follow this schema:
  {{ schema | tojson }}
  {% endif %}
  
  Provide only the converted output, no explanations.

test_cases:
  - name: "json_to_csv"
    input:
      input_format: "JSON"
      output_format: "CSV"
      data: '[{"name":"Alice","age":30},{"name":"Bob","age":25}]'
    expected_meaning:
      - "contains CSV format"
      - "includes headers"
```

## Example 3: Multi-Step Prompt

```yaml
# prompts/analysis-pipeline.yaml
id: analysis-pipeline
version: 1
model: gpt-4

variables:
  text:
    type: string
    required: true
  steps:
    type: list
    required: true
    description: "Analysis steps to perform"

template: |
  Analyze the following text through multiple steps:
  
  Text:
  """
  {{ text }}
  """
  
  Perform these analysis steps in order:
  {% for step in steps %}
  {{ loop.index }}. {{ step }}
  {% endfor %}
  
  Provide results for each step clearly labeled.

test_cases:
  - name: "sentiment_and_summary"
    input:
      text: "The product is amazing! Best purchase ever. Highly recommend."
      steps:
        - "Sentiment analysis"
        - "Key points extraction"
        - "Summary in one sentence"
    expected_meaning:
      - "identifies positive sentiment"
      - "extracts key points"
      - "provides summary"
```

