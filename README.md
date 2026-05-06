# Document Q&A App

A Streamlit-based application that allows users to upload PDF documents and ask questions about them using a retrieval-augmented generation (RAG) approach with embeddings and an LLM.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Setup Instructions

### 1. Create a Virtual Environment

Navigate to the project directory and create a virtual environment:

```bash
python -m venv .venv
```

### 2. Activate the Virtual Environment

#### On macOS/Linux:
```bash
source .venv/bin/activate
```

#### On Windows:
```bash
.venv\Scripts\activate
```

### 3. Install Dependencies

Once the virtual environment is activated, install the required packages:

```bash
pip install -r requirements.txt
```

### 4. Run the Application

Start the Streamlit app:

```bash
streamlit run app/main.py
```

The application will open in your default web browser at `http://localhost:8501`.

## Project Structure

```
.
├── app/
│   ├── main.py                 # Main Streamlit application
│   ├── llm_utils.py            # LLM utilities and model loading
│   ├── chunking/
│   │   └── chunker.py          # Document chunking logic
│   ├── generation/
│   │   └── generation.py       # Answer generation logic
│   ├── ingestion/
│   │   └── loader.py           # PDF loading and parsing
│   ├── retriever/
│   │   └── retriever.py        # Document retrieval logic
│   └── vector_store/
│       └── vector_store.py     # Vector database management
├── requirements.txt            # Project dependencies
└── README.md                   # This file
```

## Deactivating the Virtual Environment

When you're done working on the project, deactivate the virtual environment:

```bash
deactivate
```

## Troubleshooting

- **Module not found errors**: Make sure the virtual environment is activated and dependencies are installed
- **Permission errors on macOS/Linux**: Try using `sudo` if needed, or ensure proper file permissions
- **Port already in use**: Streamlit uses port 8501 by default. If it's in use, you can specify a different port:
  ```bash
  streamlit run app/main.py --server.port 8502
  ```

## Features

- Upload PDF documents
- Automatic text chunking and embedding generation
- Semantic search over document content
- RAG-based question answering using LLMs
- Vector database for efficient retrieval


## Approach

This application implements a **Retrieval-Augmented Generation (RAG)** pipeline to answer questions about uploaded PDF documents. The approach involves the following steps:

### 1. **Document Ingestion** (`ingestion/loader.py`)
   - Users upload PDF documents through the Streamlit interface
   - PDFs are parsed and converted into raw text content

### 2. **Text Chunking** (`chunking/chunker.py`)
   - Large documents are split into smaller, overlapping chunks to improve retrieval accuracy
   - Overlapping chunks ensure important information at boundaries isn't missed

### 3. **Embedding Generation** (`vector_store/vector_store.py`)
   - Each text chunk is converted into a vector embedding using a language model
   - Embeddings capture semantic meaning of the text
   - Embeddings are stored in a vector database (Chroma) for efficient retrieval

### 4. **Vector Store Management** (`vector_store/vector_store.py`)
   - Vector embeddings are persisted in a vector database
   - Database supports efficient similarity search operations
   - Enables fast retrieval of relevant chunks based on query embeddings

### 5. **Query Retrieval** (`retriever/retriever.py`)
   - User queries are converted into embeddings using the same model
   - Semantic similarity search is performed against stored embeddings
   - Top-K most relevant document chunks are retrieved

### 6. **Answer Generation** (`generation/generation.py`)
   - Retrieved chunks are passed to a Large Language Model (LLM)
   - LLM uses retrieved context to generate accurate, contextual answers

### 7. **LLM Integration** (`llm_utils.py`)
   - Manages LLM model loading and inference
   - Optimizes token usage for efficient processing

## Limitations

- **Single Model for Both Embedding and LLM**: Currently, the application uses the **all-MiniLM-L6-v2** as an embedding model and **Qwen3-0.6B** as an LLM.

- **No Evaluation Metrics**: The application lacks built-in evaluation and metrics to assess answer quality, retrieval accuracy, or overall performance. There are no automated tests to validate:
  - Relevance of retrieved documents
  - Quality of generated answers
  - Similarity between model predictions and ground truth

- **Limited Error Handling**: Edge cases such as empty documents, malformed PDFs, or queries outside document scope may not be handled gracefully.

- **No Query Rewriting**: The system performs direct semantic search without query reformulation, which may miss relevant documents when queries use different terminology.

- **Fixed Chunk Size**: Chunk size and overlap are fixed parameters. Documents with varying content density may benefit from adaptive chunking strategies.

- **No Caching**: Each query requires full embedding and retrieval operations. Caching frequently asked questions could improve performance.

- **Limited Document Types**: Currently supports only PDF files. Other formats (DOCX, TXT, etc.) are not supported.

### Future Improvements

- Implement evaluation metrics and automated testing
- Add support for multiple document formats
- We can use better embedding models with larger dimension and better llm to improve the generation part.
- Add query expansion and reformulation
- Implement response caching
- Add confidence scores to generated answers
- Support multiple vector database backends
