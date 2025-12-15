# Defining Prompts

## Basic Prompt

```yaml
# prompts/summarize.yaml
id: summarize
version: 1
model: gpt-3.5-turbo
template: |
  Summarize this text in 3 sentences:
  
  {{ text }}
```

## Prompt with Variables

Variables use Jinja2 syntax: `{{ variable_name }}`

```yaml
# prompts/translate.yaml
id: translate
version: 1
model: gpt-3.5-turbo

# Document expected variables
variables:
  target_language:
    type: string
    required: true
    description: Language to translate to
  
  text:
    type: string
    required: true
    description: Text to translate

template: |
  Translate this text to {{ target_language }}:
  
  {{ text }}
```

## Prompt with System Message

```yaml
# prompts/chatbot.yaml
id: chatbot
version: 1
model: gpt-4

system: |
  You are a helpful assistant that answers questions concisely.
  Always be polite and professional.

template: |
  {{ user_message }}
```

## Prompt with Multiple Variables

```yaml
# prompts/code-review.yaml
id: code-review
version: 2
model: gpt-4
description: Reviews code for quality, bugs, and performance

variables:
  code:
    type: string
    required: true
    description: Code to review
  
  language:
    type: string
    required: false
    default: "Python"
    description: Programming language
  
  focus_areas:
    type: list
    required: false
    default: ["quality", "bugs", "performance"]
    description: Areas to focus on

template: |
  You are reviewing {{ language }} code.
  
  Code:
  ```{{ language.lower() }}
  {{ code }}
  ```
  
  Focus on:
  {% for area in focus_areas %}
  - {{ area }}
  {% endfor %}
  
  Provide detailed feedback.
```

## Advanced Jinja2 Features

```yaml
# prompts/advanced.yaml
id: advanced
version: 1
model: gpt-4

template: |
  # Conditionals
  {% if user_type == "admin" %}
  You have admin privileges.
  {% else %}
  You have standard privileges.
  {% endif %}
  
  # Loops
  {% for item in items %}
  - {{ item.name }}: {{ item.value }}
  {% endfor %}
  
  # Filters
  {{ text | upper }}
  {{ number | round(2) }}
  
  # Default values
  {{ optional_var | default("fallback value") }}
```

