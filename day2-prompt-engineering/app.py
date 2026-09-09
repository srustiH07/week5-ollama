import requests

# Ollama API URL
URL = "http://localhost:11434/api/chat"

# Custom system prompt
SYSTEM_PROMPT = """
You are a cybersecurity tutor.
Explain cybersecurity concepts in simple English.
Use short explanations and practical examples.
Do not provide harmful instructions for performing cyber attacks.
"""

# Function to ask Ollama
def ask_ollama(prompt):
    data = {
        "model": "llama3.2:3b",
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": False
    }

    response = requests.post(URL, json=data)

    if response.status_code == 200:
        result = response.json()
        return result["message"]["content"]
    else:
        return "Error: " + str(response.status_code)


# Five test prompts
prompts = [
    "What is the CIA Triad in cybersecurity?",
    "What is a firewall?",
    "What is encryption?",
    "What is a brute-force attack?",
    "What is phishing?"
]


# Run all five prompts
for i, prompt in enumerate(prompts, 1):

    print("\n" + "=" * 60)
    print(f"PROMPT {i}")
    print("=" * 60)

    print("QUESTION:")
    print(prompt)

    print("\nRESPONSE:")
    print(ask_ollama(prompt))