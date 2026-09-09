import requests

# Ollama API endpoint
URL = "http://localhost:11434/api/generate"

# System prompt used for both models
SYSTEM_PROMPT = """
You are a helpful AI tutor.
Give accurate, clear, and easy-to-understand answers.
For programming questions, provide working Python code and explain it.
"""

# The same questions will be given to both models
questions = [
    "Explain the difference between Artificial Intelligence and Machine Learning in simple words, with one example.",
    
    "Write a Python function to check whether a number is prime and explain the code.",
    
    "Explain the CIA Triad in cybersecurity and give one practical example for each component."
]

# Models we want to compare
models = [
    "llama3.2:3b",
    "qwen2.5:3b"
]


# Function to send a question to Ollama
def ask_model(model, question):

    payload = {
        "model": model,
        "prompt": question,
        "system": SYSTEM_PROMPT,
        "stream": False
    }

    response = requests.post(URL, json=payload)

    if response.status_code == 200:
        return response.json()["response"]

    return f"Error: {response.status_code}"


# Ask all questions to both models
for question_number, question in enumerate(questions, start=1):

    print("\n" + "=" * 70)
    print(f"QUESTION {question_number}")
    print("=" * 70)

    print(question)

    for model in models:

        print("\n" + "-" * 70)
        print(f"MODEL: {model}")
        print("-" * 70)

        answer = ask_model(model, question)

        print(answer)