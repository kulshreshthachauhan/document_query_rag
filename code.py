from fastapi import FastAPI, UploadFile, File
import uvicorn
from chromadb import Client as ChromaInstance
from sentence_transformers import SentenceTransformer
from fastapi.responses import JSONResponse
from typing import List
import logging
import uuid

# Initialize FastAPI app
app = FastAPI()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger_service = logging.getLogger(_name_)

# Load SentenceTransformer model (CPU)
try:
    embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    logger_service.info("SentenceTransformer model loaded successfully.")
except Exception as model_error:
    logger_service.error(f"Model loading failed: {str(model_error)}")
    raise model_error

# Configure ChromaDB client for persistence
try:
    chroma_instance = ChromaInstance()
    document_storage = chroma_instance.get_or_create_collection(name="document_store")
    logger_service.info("ChromaDB client initialized; collection created.")
except Exception as db_init_error:
    logger_service.error(f"ChromaDB initialization error: {str(db_init_error)}")
    raise db_init_error

@app.post("/ingest/", response_class=JSONResponse)
async def add_files(file_list: List[UploadFile] = File(...)):
    """ Endpoint to ingest files for later retrieval """
    doc_items = []
    embedding_vectors = []
    doc_ids = []
    
    try:
        # Process each file and prepare for ingestion
        for uploaded_file in file_list:
            try:
                file_content = await uploaded_file.read()
                decoded_text = file_content.decode('utf-8')
                unique_id = str(uuid.uuid4())
                document_data = {"text": decoded_text, "metadata": {'filename': uploaded_file.filename}}
                doc_items.append(document_data)
                doc_ids.append(unique_id)
                logger_service.info(f"File '{uploaded_file.filename}' processed successfully.")

            except UnicodeDecodeError:
                logger_service.error(f"Cannot decode '{uploaded_file.filename}'. Unsupported format.")
                return JSONResponse(content={"error": f"Cannot decode '{uploaded_file.filename}'."}, status_code=400)
            except Exception as file_process_error:
                logger_service.error(f"Error processing file '{uploaded_file.filename}': {str(file_process_error)}")
                return JSONResponse(content={"error": f"File error: {str(file_process_error)}"}, status_code=500)

        # Generate embeddings for each document
        try:
            embedding_vectors = [embedding_model.encode(doc["text"]).tolist() for doc in doc_items]
            logger_service.info("Document embeddings generated successfully.")
        except Exception as embedding_error:
            logger_service.error(f"Error generating embeddings: {str(embedding_error)}")
            return JSONResponse(content={"error": f"Embedding error: {str(embedding_error)}"}, status_code=500)

        # Add documents to ChromaDB
        try:
            document_storage.add(ids=doc_ids, documents=[doc["text"] for doc in doc_items], 
                                 metadatas=[doc["metadata"] for doc in doc_items], embeddings=embedding_vectors)
            logger_service.info("Documents successfully added to ChromaDB.")
        except Exception as storage_error:
            logger_service.error(f"Error adding documents to database: {str(storage_error)}")
            return JSONResponse(content={"error": f"Database error: {str(storage_error)}"}, status_code=500)

        return JSONResponse(content={"status": "Documents ingested successfully"})

    except Exception as ingestion_error:
        logger_service.error(f"Unexpected error during ingestion: {str(ingestion_error)}")
        return JSONResponse(content={"error": f"Server Error: {str(ingestion_error)}"}, status_code=500)

@app.get("/query/", response_class=JSONResponse)
async def retrieve_documents(search_text: str):
    """ Endpoint to retrieve documents based on a query """
    try:
        # Generate embedding for the query
        search_vector = embedding_model.encode(search_text).tolist()
        logger_service.info("Query embedding generated successfully.")
        
        # Query ChromaDB
        query_results = document_storage.query(query_embeddings=[search_vector], n_results=5)
        formatted_results = [
            {
                "filename": meta_data.get('filename', 'unknown') if isinstance(meta_data, dict) else 'unknown',
                "score": relevance_score,
                "text": matched_doc
            }
            for meta_data, relevance_score, matched_doc in zip(query_results['metadatas'], query_results['distances'], query_results['documents'])
        ]
        logger_service.info("Query executed successfully.")
        return JSONResponse(content={"results": formatted_results})
    
    except Exception as query_error:
        logger_service.error(f"Error during query: {str(query_error)}")
        return JSONResponse(content={"error": f"Server Error: {str(query_error)}"}, status_code=500)

@app.get("/database/", response_class=JSONResponse)
async def view_all_documents():
    """ Endpoint to view all documents stored in the database """
    try:
        all_documents = document_storage.get()
        document_response = [
            {
                "filename": meta.get('filename', 'unknown') if isinstance(meta, dict) else 'unknown',
                "text": document_text
            }
            for meta, document_text in zip(all_documents['metadatas'], all_documents['documents'])
        ]
        logger_service.info("Successfully retrieved all documents.")
        return JSONResponse(content={"documents": document_response})
    except Exception as retrieval_error:
        logger_service.error(f"Error retrieving documents: {str(retrieval_error)}")
        return JSONResponse(content={"error": f"Server Error: {str(retrieval_error)}"}, status_code=500)

if _name_ == "_main_":
    # Run the FastAPI app with live-reload enabled
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
