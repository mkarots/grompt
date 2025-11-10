# Grompt Architecture Diagram

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         GROMPT SYSTEM                           │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      APPLICATION LAYER                          │
│  ┌──────────────────┐         ┌──────────────────┐            │
│  │   CLI Commands   │         │   Use Cases      │            │
│  │                  │         │                  │            │
│  │ • grompt init    │────────▶│ • LoadPrompt     │            │
│  │ • grompt add     │         │ • RenderPrompt   │            │
│  │ • grompt commit  │         │ • CountTokens    │            │
│  │ • grompt test    │         │ • ValidatePrompt │            │
│  │ • grompt count   │         │                  │            │
│  └──────────────────┘         └──────────────────┘            │
│           │                            │                        │
└───────────┼────────────────────────────┼────────────────────────┘
            │                            │
            ▼                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                         CORE LAYER                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Prompt     │  │   Template   │  │  Tokenizer   │         │
│  │   Entity     │  │   Renderer   │  │              │         │
│  │              │  │              │  │              │         │
│  │ • id         │  │ • render()   │  │ • count()    │         │
│  │ • version    │  │              │  │              │         │
│  │ • model      │  │              │  │              │         │
│  │ • template   │  │              │  │              │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
            │                            │
            ▼                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    INFRASTRUCTURE LAYER                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Storage    │  │     LLM      │  │   Testing    │         │
│  │              │  │  Integrations│  │              │         │
│  │ • YAMLLoader │  │              │  │ • Runner     │         │
│  │ • GitAdapter │  │ • OpenAI     │  │ • Validator  │         │
│  │              │  │ • Anthropic  │  │              │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│           │                 │                 │                 │
└───────────┼─────────────────┼─────────────────┼─────────────────┘
            │                 │                 │
            ▼                 ▼                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                      EXTERNAL SYSTEMS                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  File System │  │   LLM APIs   │  │     Git      │         │
│  │              │  │              │  │              │         │
│  │ prompts/*.yaml│  │ • OpenAI    │  │ • add        │         │
│  │ .grompt/     │  │ • Anthropic  │  │ • commit     │         │
│  │              │  │ • Google     │  │ • push       │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

### Loading and Rendering a Prompt

```
User Code
   │
   │ Prompt.load("code-review")
   ▼
┌──────────────────────────────────────┐
│  Application: LoadPromptUseCase      │
│  1. Receives prompt ID               │
│  2. Calls infrastructure layer       │
└──────────────────────────────────────┘
   │
   ▼
┌──────────────────────────────────────┐
│  Infrastructure: YAMLLoader          │
│  1. Reads prompts/code-review.yaml   │
│  2. Parses YAML                      │
│  3. Returns dict                     │
└──────────────────────────────────────┘
   │
   ▼
┌──────────────────────────────────────┐
│  Application: LoadPromptUseCase      │
│  1. Creates Prompt entity from dict  │
│  2. Returns Prompt object            │
└──────────────────────────────────────┘
   │
   ▼
User Code
   │
   │ prompt.render(code="...")
   ▼
┌──────────────────────────────────────┐
│  Core: TemplateRenderer              │
│  1. Takes template string            │
│  2. Renders with Jinja2              │
│  3. Returns rendered text            │
└──────────────────────────────────────┘
   │
   ▼
User Code (rendered prompt)
```

### CLI Command Flow

```
$ grompt test code-review --var code="..."
   │
   ▼
┌──────────────────────────────────────┐
│  Application: CLI Command            │
│  1. Parse arguments                  │
│  2. Extract variables                │
└──────────────────────────────────────┘
   │
   ▼
┌──────────────────────────────────────┐
│  Application: LoadPromptUseCase      │
│  1. Load prompt by ID                │
└──────────────────────────────────────┘
   │
   ▼
┌──────────────────────────────────────┐
│  Core: TemplateRenderer              │
│  1. Render template with variables   │
└──────────────────────────────────────┘
   │
   ▼
┌──────────────────────────────────────┐
│  Core: TokenCounter                  │
│  1. Count tokens in rendered text    │
└──────────────────────────────────────┘
   │
   ▼
┌──────────────────────────────────────┐
│  Application: CLI Command            │
│  1. Display results to user          │
└──────────────────────────────────────┘
```

## Layer Dependencies

```
┌─────────────────────────────────────────┐
│         APPLICATION LAYER               │
│  (Depends on Core + Infrastructure)     │
└─────────────────────────────────────────┘
              │         │
              │         │
              ▼         ▼
┌──────────────────┐  ┌──────────────────┐
│   CORE LAYER     │  │ INFRASTRUCTURE   │
│  (No deps)       │  │  (Depends on     │
│                  │  │   Core only)     │
└──────────────────┘  └──────────────────┘
```

**Dependency Rules:**
- ✅ Application → Core
- ✅ Application → Infrastructure
- ✅ Infrastructure → Core
- ❌ Core → Application (NEVER)
- ❌ Core → Infrastructure (NEVER)
- ❌ Infrastructure → Application (NEVER)

## Component Responsibilities

### Core Layer
```
┌─────────────────────────────────────────┐
│              CORE LAYER                 │
│  Pure business logic, no dependencies   │
├─────────────────────────────────────────┤
│                                         │
│  Prompt Entity                          │
│  • Data structure for prompts           │
│  • No I/O, no external calls            │
│                                         │
│  TemplateRenderer                       │
│  • Pure template rendering logic        │
│  • Uses Jinja2 (allowed dependency)     │
│                                         │
│  TokenCounter                           │
│  • Pure token counting logic            │
│  • Uses tiktoken (allowed dependency)   │
│                                         │
└─────────────────────────────────────────┘
```

### Application Layer
```
┌─────────────────────────────────────────┐
│          APPLICATION LAYER              │
│  Orchestrates core logic & infra        │
├─────────────────────────────────────────┤
│                                         │
│  CLI Commands                           │
│  • User interface                       │
│  • Argument parsing                     │
│  • Output formatting                    │
│                                         │
│  Use Cases                              │
│  • LoadPrompt                           │
│  • RenderPrompt                         │
│  • CountTokens                          │
│  • ValidatePrompt                       │
│                                         │
└─────────────────────────────────────────┘
```

### Infrastructure Layer
```
┌─────────────────────────────────────────┐
│        INFRASTRUCTURE LAYER             │
│  External system adapters               │
├─────────────────────────────────────────┤
│                                         │
│  Storage                                │
│  • YAMLLoader (file I/O)                │
│  • GitAdapter (git operations)          │
│                                         │
│  LLM Integrations                       │
│  • OpenAIAdapter                        │
│  • AnthropicAdapter                     │
│                                         │
│  Testing                                │
│  • TestRunner                           │
│  • PromptValidator                      │
│                                         │
└─────────────────────────────────────────┘
```

## File Organization

```
grompt/
│
├── core/                    # Pure domain logic
│   ├── __init__.py
│   ├── prompt.py           # Prompt entity
│   ├── template.py         # Template rendering
│   └── tokenizer.py        # Token counting
│
├── application/             # Use cases & CLI
│   ├── __init__.py
│   ├── cli/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── commands/
│   │       ├── init.py
│   │       ├── add.py
│   │       ├── commit.py
│   │       ├── test.py
│   │       └── count.py
│   │
│   └── use_cases/
│       ├── load_prompt.py
│       ├── render_prompt.py
│       └── count_tokens.py
│
└── infrastructure/          # External adapters
    ├── __init__.py
    ├── storage/
    │   ├── yaml_loader.py
    │   └── git_adapter.py
    │
    ├── llm/
    │   ├── openai.py
    │   ├── anthropic.py
    │   └── base.py
    │
    └── testing/
        ├── runner.py
        └── validator.py
```

## Benefits of This Architecture

1. **Testability**
   - Core logic is pure, easy to unit test
   - Infrastructure can be mocked
   - Application layer tests use cases

2. **Maintainability**
   - Clear separation of concerns
   - Easy to find where logic lives
   - Changes are localized

3. **Flexibility**
   - Swap infrastructure (e.g., different storage)
   - Add new LLM providers easily
   - Core logic remains unchanged

4. **Scalability**
   - Add new use cases without touching core
   - Add new CLI commands easily
   - Extend infrastructure independently