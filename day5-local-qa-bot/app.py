import ollama

# ============================================================
# W5D5 - LOCAL Q&A BOT USING OLLAMA
# ============================================================

# ------------------------------------------------------------
# Function 1: Ask a model using a custom system prompt
# ------------------------------------------------------------

def ask_model(model, question):
    system_prompt = """
You are a helpful AI/ML mentor.
Answer questions clearly and simply.
Give accurate and concise explanations.
If the question is related to cybersecurity or programming,
include a small example when useful.
"""

    response = ollama.chat(
        model=model,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )

    return response["message"]["content"]


# ------------------------------------------------------------
# Five prompts for testing
# ------------------------------------------------------------

prompts = [
    "What is artificial intelligence?",
    "What is machine learning?",
    "What is a firewall?",
    "What is encryption?",
    "What is a brute-force attack?"
]


# ------------------------------------------------------------
# Test Llama 3.2
# ------------------------------------------------------------

print("=" * 60)
print("W5D5 - LOCAL Q&A BOT")
print("=" * 60)

print("\nMODEL: llama3.2:3b")
print("-" * 60)

for i, prompt in enumerate(prompts, start=1):
    print(f"\nPROMPT {i}: {prompt}")
    print("RESPONSE:")

    answer = ask_model("llama3.2:3b", prompt)

    print(answer)
    print("-" * 60)


# ------------------------------------------------------------
# Compare Llama 3.2 and Qwen 2.5
# ------------------------------------------------------------

comparison_questions = [
    "What is artificial intelligence?",
    "What is a firewall?",
    "What is encryption?"
]

print("\n")
print("=" * 60)
print("MODEL COMPARISON")
print("=" * 60)

for i, question in enumerate(comparison_questions, start=1):

    print(f"\nQUESTION {i}: {question}")
    print("=" * 60)

    print("\nLLAMA 3.2:3B")
    print("-" * 30)

    llama_answer = ask_model(
        "llama3.2:3b",
        question
    )

    print(llama_answer)

    print("\nQWEN 2.5:3B")
    print("-" * 30)

    qwen_answer = ask_model(
        "qwen2.5:3b",
        question
    )

    print(qwen_answer)

    print("\n" + "=" * 60)


print("\nW5D5 execution completed successfully!")