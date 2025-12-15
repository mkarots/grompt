import grompt
import sys

try:
    # Test grompt.load
    prompt = grompt.load("test-prompt", prompts_dir="test_prompts")
    print(f"Loaded prompt: {prompt.id}")
    
    # Test prompt.render
    rendered = prompt.render(name="World")
    print(f"Rendered output: {rendered.strip()}")
    
    if rendered.strip() == "Hello World!":
        print("SUCCESS")
    else:
        print("FAILURE: Rendered output mismatch")
        sys.exit(1)
        
except Exception as e:
    print(f"FAILURE: {e}")
    sys.exit(1)

