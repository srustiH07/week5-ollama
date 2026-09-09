# Llama 3.2:3B vs Qwen 2.5:3B Comparison

## Objective

The objective is to compare the response quality of two locally running
Large Language Models using Ollama:

- Llama 3.2:3B
- Qwen 2.5:3B

Both models were given the same questions and the same system prompt.

## Questions Tested

1. Explain the difference between Artificial Intelligence and Machine
   Learning in simple words, with one example.

2. Write a Python function to check whether a number is prime and explain
   the code.

3. Explain the CIA Triad in cybersecurity and give one practical example
   for each component.

## Comparison Criteria

The models were compared based on:

- Accuracy
- Clarity
- Level of detail
- Examples
- Technical correctness
- Overall usefulness

## Question 3: CIA Triad

### Llama 3.2:3B

Llama 3.2:3B gave a detailed explanation of Confidentiality, Integrity,
and Availability.

It provided practical examples for each component:

- Confidentiality: protecting sensitive employee information using
  encryption.
- Integrity: protecting password-related data using hashing.
- Availability: monitoring a cloud application and using backup
  processes during outages.

The response was detailed and explained how each component contributes
to cybersecurity.

### Qwen 2.5:3B

Qwen 2.5:3B also correctly explained Confidentiality, Integrity, and
Availability.

Its examples included:

- Confidentiality: protecting banking account information.
- Integrity: using digital signatures to detect changes to financial
  transactions.
- Availability: using a backup power generator in a hospital.

The response was structured clearly and provided practical examples.

## Observations

| Criteria              | Llama 3.2:3B     | Qwen 2.5:3B     |
| --------------------- | ---------------- | --------------- |
| Accuracy              | Good             | Good            |
| Clarity               | Very clear       | Very clear      |
| Detail                | High             | High            |
| Examples              | Practical        | Practical       |
| Technical explanation | Detailed         | Detailed        |
| Response style        | More explanatory | More structured |

## Overall Comparison

Both models successfully answered the cybersecurity question and provided
useful practical examples.

Llama 3.2:3B provided a more explanatory response with detailed
descriptions of each CIA component.

Qwen 2.5:3B presented the concepts in a structured way and used practical
examples from banking, financial transactions, and healthcare.

Based on this test, both models performed well. The differences in
response quality were relatively small, and the preferred model may
depend on whether the user prefers more detailed explanations or a more
structured response.

## Conclusion

Both Llama 3.2:3B and Qwen 2.5:3B can be used for local AI inference
through Ollama. The comparison demonstrated that different local LLMs
can produce different styles of responses even when they receive the
same prompt.
