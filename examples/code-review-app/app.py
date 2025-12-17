"""
Example: Code Review Assistant using Grompt

This demonstrates how to use Grompt in a real application.
The prompts are stored separately and can be changed without modifying this code.
"""

import grompt
from pathlib import Path


def review_code(code: str, language: str = "Python") -> str:
    """
    Review code using a prompt loaded from Grompt.
    
    Args:
        code: The code to review
        language: Programming language
        
    Returns:
        Review feedback (in a real app, this would call an LLM)
    """
    # Load the prompt - no hardcoded strings!
    prompt = grompt.load("code-review")
    
    # Render with variables
    rendered = prompt.render(
        code=code,
        language=language
    )
    
    # In a real app, you'd call your LLM API here
    # For this example, we'll just return the rendered prompt
    print("=" * 60)
    print("PROMPT TO SEND TO LLM:")
    print("=" * 60)
    print(rendered)
    print("=" * 60)
    
    return rendered


def main():
    """Example usage."""
    print("Code Review Assistant Example\n")
    
    # Example code snippets to review
    examples = [
        {
            "code": "def add(a, b): return a + b",
            "language": "Python",
            "description": "Simple function"
        },
        {
            "code": "def divide(x, y): return x / y",
            "language": "Python", 
            "description": "Division function (potential bug)"
        },
        {
            "code": """
def process_user_input(user_input):
    query = f"SELECT * FROM users WHERE id={user_input}"
    return execute_query(query)
            """.strip(),
            "language": "Python",
            "description": "SQL injection vulnerability"
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n[{i}] Reviewing: {example['description']}")
        print(f"Code: {example['code']}\n")
        review_code(example['code'], example['language'])
        print()


if __name__ == "__main__":
    main()

