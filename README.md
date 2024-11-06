# FastAPI Server for Retrieval-Augmented Generation (RAG)

This repository provides a lightweight FastAPI server built for Retrieval-Augmented Generation (RAG), allowing document ingestion and retrieval. Utilizing ChromaDB for efficient data storage and query capabilities, this server supports PDF, DOC, DOCX, and TXT formats. Document embeddings are generated using the sentence-transformers/all-MiniLM-L6-v2 model, optimized for CPU use, with non-blocking endpoints to handle concurrent requests effectively.

## Features
- *Document Storage & Search*: Ingest and search documents (PDF, DOC, DOCX, TXT) with ChromaDB.
- *High-Quality Embeddings*: Uses sentence-transformers/all-MiniLM-L6-v2 for semantic text embeddings.
- *Concurrent API*: FastAPI provides responsive, non-blocking endpoints for efficient request handling.

## Tech Stack
- *FastAPI*: Framework for API development.
- *ChromaDB*: Stores and retrieves document embeddings.
- *Sentence-Transformers*: Embedding generation using all-MiniLM-L6-v2.
- *Python*: Core programming language.
- *Uvicorn*: ASGI server for FastAPI app deployment.

## Libraries and Tools
1. *FastAPI*: Fast, asynchronous web framework for APIs.
2. *Uvicorn*: High-performance ASGI server for FastAPI.
3. *ChromaDB*: Vector database for managing document embeddings.
4. *Sentence-Transformers*: Embedding generation with transformer models.
5. *Langchain*: Simplifies document loading and processing.
6. *Python Standard Libraries*: Utilities like uuid for unique IDs and logging for tracking.

## Getting Started
### Prerequisites
- Python 3.8+
- pip for installing packages

### Installation
1. *Clone the Repository*
   sh
   git clone https://github.com/<username>/fastapi-rag-server.git
   cd fastapi-rag-server
   

2. *Install Required Packages*
   sh
   pip install -r requirements.txt
   

3. *Run the Server*
   sh
   uvicorn main:app --reload
   
   Access the server at http://127.0.0.1:8000.

## API Endpoints
### 1. /ingest/ [POST]
Uploads documents (PDF, DOC, DOCX, TXT) to the database.
- *Request*: Multipart form with files.
- *Example Files*: sample1.txt, sample2.pdf
- *Sample Response*:
  json
  { "status": "Documents uploaded successfully" }
  

### 2. /query/ [GET]
Searches stored documents for a query.
- *Parameter*: query_text (str) - The text to search for.
- *Sample URL*: http://127.0.0.1:8000/query/?query_text=What is FastAPI?
- *Sample Response*:
  json
  {
    "results": [
      {
        "filename": "sample1.txt",
        "score": 0.7214,
        "text": "Title: Introduction to FastAPI\n\nFastAPI is a modern, high-performance web framework..."
      }
    ]
  }
  

### 3. /database/ [GET]
Fetches all stored documents with metadata and text.
- *Sample Response*:
  json
  {
    "documents": [
      { "filename": "sample1.txt", "text": "Introduction to FastAPI..." },
      { "filename": "sample2.pdf", "text": "Sample PDF document content..." }
    ]
  }
  

## Running the Server
1. *Start the Server*
   sh
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   
   - The server will be available at http://localhost:8000.

2. *Testing Endpoints*
   - Use tools like *Postman* or *Thunder Client* for testing requests.

## Usage Example
### Ingest Documents
Upload documents with a POST request to /ingest/.
- *URL*: http://localhost:8000/ingest/
- *Method*: POST with files in form-data.

### Query Documents
Send a GET request to /query/ with your search term.
- *URL*: http://localhost:8000/query/?query_text=<your_query>

## Contributing
Contributions are welcome! Please submit a Pull Request.

For questions, reach out to [kulshreshthachauhan12@gmail.com](mailto:kulshreshthachauhan12@gmail.com) or visit [kulshreshthachauhan](https://github.com/kulshreshthachauhan).

## License
This project is licensed under the MIT License.

## Acknowledgements
- [FastAPI](https://fastapi.tiangolo.com/)
- [ChromaDB](https://github.com/chroma-core/chroma)
- [Sentence-Transformers](https://www.sbert.net/)
- [Langchain](https://langchain.com/)
