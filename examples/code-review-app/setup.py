"""
Setup script for the example app.
Creates a Grompt project and adds a code-review prompt.
"""

import subprocess
import sys
from pathlib import Path


def setup_example():
    """Set up the example Grompt project."""
    example_dir = Path(__file__).parent
    
    print("Setting up Grompt example...")
    print(f"Working directory: {example_dir}\n")
    
    # Initialize Grompt
    print("1. Initializing Grompt...")
    subprocess.run(
        ["grompt", "init", "--prompts-dir", "prompts"],
        cwd=example_dir,
        check=True
    )
    
    # Create a code-review prompt
    print("\n2. Creating code-review prompt...")
    subprocess.run(
        [
            "grompt", "add", "code-review",
            "--template", """You are an expert code reviewer. Review the following {{ language }} code:

```{{ language.lower() }}
{{ code }}
```

Provide feedback on:
1. Code quality and readability
2. Potential bugs or edge cases
3. Security issues
4. Best practices

Be constructive and specific.""",
            "--description", "Code review prompt for analyzing code quality"
        ],
        cwd=example_dir,
        check=True
    )
    
    print("\n✅ Setup complete!")
    print("\nTo run the example:")
    print(f"  cd {example_dir}")
    print("  python app.py")
    print("\nTo modify the prompt:")
    print("  grompt add code-review --template 'Your new template here'")
    print("  (or edit prompts/code-review.yaml directly)")


if __name__ == "__main__":
    try:
        setup_example()
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("\n❌ Error: 'grompt' command not found.", file=sys.stderr)
        print("Install Grompt first: pip install grompt", file=sys.stderr)
        sys.exit(1)

