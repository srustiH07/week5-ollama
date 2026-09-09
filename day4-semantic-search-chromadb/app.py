import chromadb
from chromadb.utils import embedding_functions
from pypdf import PdfReader
import ollama
import os

print("=" * 60)
print("W5D4: SEMANTIC SEARCH WITH CHROMADB")
print("=" * 60)

# ---------------------------------------------------------
# 1. CREATE CHROMADB COLLECTION
# ---------------------------------------------------------

client = chromadb.PersistentClient(path="./chroma_db")

embedding_function = embedding_functions.DefaultEmbeddingFunction()

collection = client.get_or_create_collection(
    name="semantic_search_collection",
    embedding_function=embedding_function,
    metadata={"hnsw:space": "cosine"}
)

print("\nChromaDB collection created successfully!")


# ---------------------------------------------------------
# 2. ADD 20 DOCUMENTS WITH EMBEDDINGS
# ---------------------------------------------------------

documents = [
    "Confidentiality protects sensitive information from unauthorized access.",
    "Integrity ensures that information remains accurate and unchanged.",
    "Availability ensures that authorized users can access systems when needed.",
    "Encryption converts readable information into protected ciphertext.",
    "Authentication verifies the identity of a user.",
    "Authorization determines what resources a user can access.",
    "A firewall monitors and controls incoming and outgoing network traffic.",
    "An intrusion detection system identifies suspicious network activity.",
    "An intrusion prevention system detects and blocks malicious traffic.",
    "Network segmentation separates systems to reduce the impact of attacks.",
    "Strong passwords help protect accounts from unauthorized access.",
    "Multi-factor authentication provides an additional layer of security.",
    "Regular software updates help fix known security vulnerabilities.",
    "Backups help organizations recover data after security incidents.",
    "Phishing attacks attempt to trick users into revealing sensitive information.",
    "Malware is malicious software designed to damage or compromise systems.",
    "A denial-of-service attack attempts to make a service unavailable.",
    "Security awareness training helps employees recognize cyber threats.",
    "Access control limits system resources to authorized users.",
    "Security monitoring helps detect suspicious activities and incidents."
]

categories = [
    "CIA Triad",
    "CIA Triad",
    "CIA Triad",
    "Cryptography",
    "Authentication",
    "Authorization",
    "Network Security",
    "Network Security",
    "Network Security",
    "Network Security",
    "Authentication",
    "Authentication",
    "Security Management",
    "Security Management",
    "Cyber Threats",
    "Cyber Threats",
    "Cyber Threats",
    "Security Management",
    "Authorization",
    "Security Monitoring"
]

ids = [f"doc_{i+1}" for i in range(20)]

collection.upsert(
    ids=ids,
    documents=documents,
    metadatas=[{"category": category} for category in categories]
)

print("20 documents added successfully!")


# ---------------------------------------------------------
# 3. SEMANTIC SEARCH USING COSINE SIMILARITY
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("SEMANTIC SEARCH - COSINE SIMILARITY")
print("=" * 60)

query = "How can I protect confidential information?"

results = collection.query(
    query_texts=[query],
    n_results=3
)

print(f"\nQuery: {query}")

for i, document in enumerate(results["documents"][0]):
    distance = results["distances"][0][i]

    print(f"\nResult {i + 1}:")
    print(f"Document: {document}")
    print(f"Cosine distance: {distance:.4f}")


# ---------------------------------------------------------
# 4. METADATA FILTERING
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("METADATA FILTERING")
print("=" * 60)

query = "How can I protect a computer network?"

filtered_results = collection.query(
    query_texts=[query],
    n_results=3,
    where={"category": "Network Security"}
)

print(f"\nQuery: {query}")
print("Filter: category = Network Security")

for i, document in enumerate(filtered_results["documents"][0]):
    print(f"\nFiltered Result {i + 1}:")
    print(f"Document: {document}")
    print(f"Metadata: {filtered_results['metadatas'][0][i]}")


# ---------------------------------------------------------
# 5. LOAD PDF
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("PDF SEMANTIC SEARCH")
print("=" * 60)

pdf_path = "cybersecurity.pdf"

if not os.path.exists(pdf_path):
    print("\nERROR: cybersecurity.pdf was not found.")
    print("Place the PDF inside the project folder and run again.")
    exit()

reader = PdfReader(pdf_path)

print(f"\nPDF loaded successfully!")
print(f"Number of pages: {len(reader.pages)}")


# ---------------------------------------------------------
# 6. EXTRACT PDF TEXT
# ---------------------------------------------------------

full_text = ""

for page in reader.pages:
    text = page.extract_text()

    if text:
        full_text += text + "\n"


# ---------------------------------------------------------
# 7. CREATE TEXT CHUNKS
# ---------------------------------------------------------

chunk_size = 1000
overlap = 100

chunks = []

start = 0

while start < len(full_text):
    end = start + chunk_size
    chunk = full_text[start:end].strip()

    if chunk:
        chunks.append(chunk)

    start += chunk_size - overlap

print(f"Created {len(chunks)} PDF chunks.")


# ---------------------------------------------------------
# 8. STORE PDF CHUNKS IN CHROMADB
# ---------------------------------------------------------

pdf_collection = client.get_or_create_collection(
    name="pdf_semantic_collection",
    embedding_function=embedding_function,
    metadata={"hnsw:space": "cosine"}
)

pdf_ids = [f"pdf_chunk_{i+1}" for i in range(len(chunks))]

pdf_collection.upsert(
    ids=pdf_ids,
    documents=chunks,
    metadatas=[
        {"source": "cybersecurity.pdf", "chunk": i + 1}
        for i in range(len(chunks))
    ]
)

print("PDF chunks added to ChromaDB successfully!")


# ---------------------------------------------------------
# 9. RETRIEVE TOP-3 RELEVANT CHUNKS
# ---------------------------------------------------------

question = "What are the main cybersecurity practices recommended for protecting an organization?"

retrieved = pdf_collection.query(
    query_texts=[question],
    n_results=3
)

print("\n" + "=" * 60)
print("TOP-3 RETRIEVED PDF CHUNKS")
print("=" * 60)

context_parts = []

for i, chunk in enumerate(retrieved["documents"][0]):
    print(f"\n--- Retrieved Chunk {i + 1} ---")
    print(chunk[:1500])

    context_parts.append(chunk)

context = "\n\n".join(context_parts)


# ---------------------------------------------------------
# 10. SEND RETRIEVED CONTEXT TO OLLAMA
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("OLLAMA RESPONSE")
print("=" * 60)

prompt = f"""
Answer the question using only the retrieved cybersecurity document
context provided below.

Question:
{question}

Retrieved Context:
{context}

Give a clear and concise answer.
"""

try:
    response = ollama.chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "system",
                "content": "You are a cybersecurity assistant. Answer using the provided document context."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    print("\nQuestion:")
    print(question)

    print("\nAnswer:")
    print(response["message"]["content"])

except Exception as error:
    print("\nOllama error:")
    print(error)


# ---------------------------------------------------------
# 11. FINAL STATUS
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("W5D4 FINAL STATUS")
print("=" * 60)

print("ChromaDB vector store: SUCCESS")
print("20 documents with embeddings: SUCCESS")
print("Cosine semantic search: SUCCESS")
print("Metadata filtering: SUCCESS")
print("PDF embedding: SUCCESS")
print("Top-3 semantic retrieval: SUCCESS")
print("Ollama integration: TESTED")