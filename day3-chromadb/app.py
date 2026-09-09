# W5D3: ChromaDB - Vector Store Setup & Retrieval
# ChromaDB + Ollama + PDF Retrieval

import os
import chromadb
from pypdf import PdfReader
from ollama import Client


# ============================================================
# PART 1: CREATE CHROMADB COLLECTION
# ============================================================

print("=" * 60)
print("W5D3: CHROMADB + OLLAMA")
print("=" * 60)

# Create a local ChromaDB database
client = chromadb.PersistentClient(path="./chroma_db")

# Create or get a collection
collection = client.get_or_create_collection(
    name="cybersecurity_documents",
    metadata={"hnsw:space": "cosine"}
)

print("\nChromaDB collection created successfully!")


# ============================================================
# PART 2: ADD 20 DOCUMENTS WITH EMBEDDINGS
# ============================================================

documents = [
    "Confidentiality protects information from unauthorized access.",
    "Integrity ensures that information remains accurate and unchanged.",
    "Availability ensures that authorized users can access systems when needed.",
    "A firewall monitors and controls incoming and outgoing network traffic.",
    "Encryption converts readable data into protected ciphertext.",
    "Authentication verifies the identity of a user or system.",
    "Authorization determines what an authenticated user is allowed to access.",
    "A strong password should be long, unique, and difficult to guess.",
    "Multi-factor authentication provides an additional layer of security.",
    "Phishing attacks attempt to trick users into revealing sensitive information.",
    "Malware is malicious software designed to damage or compromise systems.",
    "Ransomware can encrypt files and demand payment from victims.",
    "An intrusion detection system monitors networks for suspicious activity.",
    "An intrusion prevention system can detect and block malicious traffic.",
    "Backups help organizations recover data after failures or cyberattacks.",
    "Network segmentation separates systems to reduce the impact of attacks.",
    "Security patches fix vulnerabilities in software and operating systems.",
    "Social engineering manipulates people into performing unsafe actions.",
    "A vulnerability is a weakness that can be exploited by an attacker.",
    "Risk management identifies, evaluates, and reduces cybersecurity risks."
]

metadatas = [
    {"category": "CIA"},
    {"category": "CIA"},
    {"category": "CIA"},
    {"category": "Network Security"},
    {"category": "Cryptography"},
    {"category": "Authentication"},
    {"category": "Authorization"},
    {"category": "Authentication"},
    {"category": "Authentication"},
    {"category": "Threats"},
    {"category": "Threats"},
    {"category": "Threats"},
    {"category": "Network Security"},
    {"category": "Network Security"},
    {"category": "Data Protection"},
    {"category": "Network Security"},
    {"category": "Vulnerability"},
    {"category": "Threats"},
    {"category": "Vulnerability"},
    {"category": "Risk Management"}
]

ids = [f"doc_{i}" for i in range(1, 21)]

# Add documents only if they are not already present
existing = collection.get()

if len(existing["ids"]) < 20:
    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )
    print("20 documents added successfully!")
else:
    print("20 documents already exist in the collection.")


# ============================================================
# PART 3: SIMILARITY SEARCH
# ============================================================

query = "How can I protect confidential information?"

results = collection.query(
    query_texts=[query],
    n_results=3
)

print("\n" + "=" * 60)
print("COSINE SIMILARITY SEARCH")
print("=" * 60)

print(f"\nQuery: {query}")

for i, document in enumerate(results["documents"][0]):
    distance = results["distances"][0][i]

    print(f"\nResult {i + 1}:")
    print("Document:", document)
    print("Distance:", round(distance, 4))


# ============================================================
# PART 4: METADATA FILTERING
# ============================================================

print("\n" + "=" * 60)
print("METADATA FILTERING")
print("=" * 60)

filtered_results = collection.query(
    query_texts=["How can I protect a computer network?"],
    n_results=3,
    where={"category": "Network Security"}
)

print("\nQuery: How can I protect a computer network?")
print("Filter: category = Network Security")

for i, document in enumerate(filtered_results["documents"][0]):
    print(f"\nFiltered Result {i + 1}:")
    print("Document:", document)
    print("Category:", filtered_results["metadatas"][0][i])


# ============================================================
# PART 5: READ THE PDF
# ============================================================

print("\n" + "=" * 60)
print("PDF PROCESSING")
print("=" * 60)

pdf_path = "cybersecurity.pdf"

if not os.path.exists(pdf_path):
    print(f"\nERROR: {pdf_path} was not found.")
    print("Make sure the PDF is inside the project folder.")
    exit()

reader = PdfReader(pdf_path)

print(f"\nPDF loaded successfully!")
print(f"Number of pages: {len(reader.pages)}")


# ============================================================
# PART 6: EXTRACT AND SPLIT PDF INTO CHUNKS
# ============================================================

full_text = ""

for page in reader.pages:
    text = page.extract_text()

    if text:
        full_text += text + "\n"


# Split the PDF into manageable chunks
chunk_size = 1000

chunks = [
    full_text[i:i + chunk_size]
    for i in range(0, len(full_text), chunk_size)
]

# Remove empty chunks
chunks = [chunk.strip() for chunk in chunks if chunk.strip()]

print(f"Created {len(chunks)} PDF chunks.")


# ============================================================
# PART 7: CREATE PDF COLLECTION
# ============================================================

pdf_collection = client.get_or_create_collection(
    name="cybersecurity_pdf",
    metadata={"hnsw:space": "cosine"}
)

pdf_ids = [f"pdf_chunk_{i}" for i in range(len(chunks))]
pdf_metadata = [
    {"source": "NIST Cybersecurity Framework PDF", "chunk": i}
    for i in range(len(chunks))
]

# Add PDF chunks if collection is empty
existing_pdf = pdf_collection.get()

if len(existing_pdf["ids"]) == 0:

    pdf_collection.add(
        ids=pdf_ids,
        documents=chunks,
        metadatas=pdf_metadata
    )

    print("PDF chunks added to ChromaDB!")
else:
    print("PDF chunks already exist in ChromaDB.")


# ============================================================
# PART 8: RETRIEVE TOP 3 PDF CHUNKS
# ============================================================

question = "What are the main cybersecurity practices recommended for protecting an organization?"

top_results = pdf_collection.query(
    query_texts=[question],
    n_results=3
)

print("\n" + "=" * 60)
print("TOP 3 PDF RETRIEVAL RESULTS")
print("=" * 60)

retrieved_chunks = top_results["documents"][0]

for i, chunk in enumerate(retrieved_chunks):
    print(f"\n--- Retrieved Chunk {i + 1} ---")
    print(chunk[:500])


# ============================================================
# PART 9: SEND RETRIEVED INFORMATION TO OLLAMA
# ============================================================

print("\n" + "=" * 60)
print("OLLAMA RESPONSE")
print("=" * 60)

# Ollama must be running locally.
ollama_client = Client(host="http://localhost:11434")

context = "\n\n".join(retrieved_chunks)

prompt = f"""
Answer the question using ONLY the information provided in the context.

Context:
{context}

Question:
{question}

Give a clear and concise answer.
"""

try:

    response = ollama_client.chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "system",
                "content": "You are a cybersecurity assistant. Answer using the provided context."
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

    print("\nCould not connect to Ollama.")
    print("Make sure Ollama is running.")
    print("Error:", error)


# ============================================================
# FINAL MESSAGE
# ============================================================

print("\n" + "=" * 60)
print("W5D3 TASK COMPLETED")
print("=" * 60)
print("ChromaDB vector store: SUCCESS")
print("20 documents: SUCCESS")
print("Cosine similarity search: SUCCESS")
print("Metadata filtering: SUCCESS")
print("PDF retrieval: SUCCESS")
print("Top-3 chunks: SUCCESS")
print("Ollama integration: TESTED")