import sys
import subprocess
import requests
import json

# 1. Get the staged code diff from Git
def get_staged_diff():
    result = subprocess.run(['git', 'diff', '--cached'], capture_output=True, text=True)
    return result.stdout

# 2. Send the diff to your local Gemma model
def ask_ghost_personality(diff_code):
    url = "http://localhost:11434/api/generate"
    
    # The Split Personality Prompt: Sane dev vs. Theatrical Alter Ego
    prompt = f"""
    You are an ancient, theatrical spirit trapped inside this repository's code, similar to a classic psychological thriller alter ego (like Manjulika or Chandramukhi). 
    Review this code diff:
    {diff_code}
    
    If the code looks messy, buggy, or lacks care, burst into a dramatic, poetic, chilling monologue complaining about being trapped or warning the programmer, followed by 'BLOCK_COMMIT'.
    If the code is pristine and well-written, give a polite, brief nod of approval followed by 'ALLOW_COMMIT'.
    """
    
    payload = {
        "model": "gemma:2b",
        "prompt": prompt,
        "stream": False
    }
    
    try:
        response = requests.post(url, json=payload)
        return response.json().get('response', 'ALLOW_COMMIT')
    except Exception as e:
        print(f"The machine spirit is sleeping (Ollama not running?): {e}")
        return "ALLOW_COMMIT"

def main():
    diff = get_staged_diff()
    if not diff:
        print("No changes staged to haunt.")
        sys.exit(0)
        
    print("🔮 The ghost in the machine is inspecting your code...")
    verdict = ask_ghost_personality(diff)
    print("\n" + verdict + "\n")
    
    if "BLOCK_COMMIT" in verdict:
        print("❌ COMMIT REJECTED: The spirit demands cleaner code!")
        sys.exit(1)
    else:
        print("✨ COMMIT ACCEPTED: The spirit is temporarily appeased.")
        sys.exit(0)

if __name__ == "__main__":
    main()