"""
Enhanced example: Code Review Assistant with OpenAI integration

This shows a complete example with:
- Prompt loading from Grompt
- Real OpenAI API integration
- Error handling
- Few-shot examples support
"""

import os
import grompt
from typing import Optional, List

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class CodeReviewer:
    """Code reviewer that uses Grompt-managed prompts with OpenAI."""
    
    def __init__(self, prompts_dir: str = "prompts", api_key: Optional[str] = None):
        """
        Initialize the reviewer.
        
        Args:
            prompts_dir: Directory containing prompt files
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
        """
        self.prompts_dir = prompts_dir
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        
        if OPENAI_AVAILABLE and self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None
    
    def review(
        self, 
        code: str, 
        language: str = "Python", 
        examples: Optional[List[str]] = None
    ) -> dict:
        """
        Review code using a Grompt prompt with OpenAI.
        
        Args:
            code: Code to review
            language: Programming language
            examples: Optional list of few-shot examples
            
        Returns:
            Dictionary with review results
        """
        # Load prompt - stored separately, versioned with git
        prompt = grompt.load("code-review", prompts_dir=self.prompts_dir)
        
        # Render with variables (including examples if provided)
        rendered = prompt.render(
            code=code,
            language=language,
            examples=examples or []
        )
        
        # Call OpenAI API
        if self.client:
            response = self._call_openai(prompt, rendered)
        else:
            response = self._fallback_response(code, language)
        
        return {
            "prompt_used": prompt.id,
            "prompt_version": prompt.version,
            "model": prompt.parameters.get("model", "unknown"),
            "review": response,
            "rendered_prompt": rendered
        }
    
    def _call_openai(self, prompt: grompt.Prompt, rendered_text: str) -> str:
        """Call OpenAI API with the rendered prompt."""
        model = prompt.parameters.get("model", "gpt-4")
        temperature = prompt.parameters.get("temperature", 0.7)
        
        messages = []
        
        # Add system message if present
        if prompt.system:
            messages.append({"role": "system", "content": prompt.system})
        
        # Add user message with rendered prompt
        messages.append({"role": "user", "content": rendered_text})
        
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=prompt.parameters.get("max_tokens", 1000)
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ Error calling OpenAI API: {str(e)}"
    
    def _fallback_response(self, code: str, language: str) -> str:
        """Fallback response when OpenAI is not available."""
        if not OPENAI_AVAILABLE:
            return "⚠️ OpenAI library not installed. Install with: pip install openai"
        if not self.api_key:
            return "⚠️ OpenAI API key not found. Set OPENAI_API_KEY environment variable."
        
        issues = []
        if "def divide" in code and "/" in code and "ZeroDivisionError" not in code:
            issues.append("⚠️ Potential division by zero error")
        
        if "f'SELECT" in code or "f\"SELECT" in code:
            issues.append("🚨 SQL injection vulnerability detected")
        
        if len(code.split('\n')) < 3 and "def" in code:
            issues.append("💡 Consider adding docstrings and type hints")
        
        if issues:
            return "\n".join(issues)
        return "✅ Code looks good! No obvious issues detected."


def main():
    """Run example reviews."""
    print("=" * 70)
    print("Code Review Assistant - Grompt Example with OpenAI")
    print("=" * 70)
    print("\nThis demonstrates:")
    print("  • Prompts stored separately from code")
    print("  • Easy to change prompts without code changes")
    print("  • Version tracking for prompts")
    print("  • Real OpenAI API integration")
    print("  • Few-shot examples support\n")
    
    # Initialize reviewer
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️  Note: OPENAI_API_KEY not set. Using fallback mode.")
        print("   Set it to use real OpenAI API: export OPENAI_API_KEY=your_key\n")
    
    reviewer = CodeReviewer()
    
    # Define few-shot examples for the reviewer
    few_shot_examples = [
        """Code:
def safe_divide(x, y):
    if y == 0:
        raise ValueError("Cannot divide by zero")
    return x / y

Review: Good error handling for division by zero. Consider adding type hints and docstring.""",
        """Code:
def get_user(user_id):
    return db.execute("SELECT * FROM users WHERE id=?", (user_id,))

Review: Excellent use of parameterized queries to prevent SQL injection. Well done!"""
    ]
    
    test_cases = [
        {
            "name": "Simple addition function",
            "code": "def add(a, b): return a + b",
            "language": "Python",
            "examples": few_shot_examples
        },
        {
            "name": "Division without error handling",
            "code": "def divide(x, y): return x / y",
            "language": "Python",
            "examples": few_shot_examples
        },
        {
            "name": "SQL injection vulnerability",
            "code": """def get_user(user_id):
    query = f"SELECT * FROM users WHERE id={user_id}"
    return db.execute(query)""",
            "language": "Python",
            "examples": few_shot_examples
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'='*70}")
        print(f"Test {i}: {test['name']}")
        print(f"{'='*70}")
        print(f"\nCode:\n{test['code']}\n")
        
        result = reviewer.review(
            code=test['code'],
            language=test['language'],
            examples=test.get('examples')
        )
        
        print(f"Prompt ID: {result['prompt_used']}")
        print(f"Prompt Version: {result['prompt_version']}")
        print(f"Model: {result['model']}")
        print(f"\nReview Result:\n{result['review']}")
        
        if i == 1:  # Show full prompt for first example
            print(f"\n--- Full Rendered Prompt (sent to LLM) ---")
            print(result['rendered_prompt'])
        else:
            print(f"\n--- Rendered Prompt Preview ---")
            print(result['rendered_prompt'][:300] + "...")
    
    print("\n" + "=" * 70)
    print("💡 Try modifying prompts/code-review.yaml and run again!")
    print("   The code stays the same, but the prompt changes.")
    print("=" * 70)


if __name__ == "__main__":
    main()

