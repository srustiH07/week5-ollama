# Week 5 Day 3 - ChromaDB Vector Store & Retrieval

## Objective

Implemented a ChromaDB vector store with document embeddings, similarity search, metadata filtering, PDF retrieval, and Ollama integration.

## Technologies Used

- Python
- ChromaDB
- Ollama
- Llama 3.2
- PyPDF
- Sentence Transformers / ONNX embeddings

## Tasks Completed

### 1. ChromaDB Vector Store

- Created a ChromaDB collection.
- Added 20 cybersecurity documents.
- Generated embeddings for the documents.

### 2. Similarity Search

- Implemented cosine similarity search.
- Tested semantic queries and verified the retrieved results.

### 3. Metadata Filtering

- Added category metadata.
- Tested filtering using the `Network Security` category.

### 4. PDF Retrieval

- Loaded a cybersecurity PDF.
- Extracted text from 32 pages.
- Split the document into 70 chunks.
- Stored the chunks in ChromaDB.
- Retrieved the top-3 relevant chunks.

### 5. Ollama Integration

- Connected the retrieved PDF chunks with Ollama.
- Used the retrieved context to generate an answer.

## Output Evidence

The `output_evidence.png` file contains evidence of the successful execution.

## Result

- ChromaDB vector store: SUCCESS
- 20 documents: SUCCESS
- Cosine similarity search: SUCCESS
- Metadata filtering: SUCCESS
- PDF retrieval: SUCCESS
- Top-3 chunks: SUCCESS
- Ollama integration: TESTED

## Viva Preparation

### 1. What is cosine similarity?

Cosine similarity measures how similar two vectors are by comparing the angle between them. It is commonly used for semantic search because similar meanings produce vectors pointing in similar directions.

### 2. What is an embedding?

An embedding is a numerical vector representation of data such as text. It captures semantic meaning and allows similar documents to be found using vector search.

### 3. ChromaDB vs FAISS

ChromaDB provides a convenient vector database with collections and metadata support. FAISS is primarily a high-performance library for efficient similarity search and gives more low-level control.
