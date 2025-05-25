import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import torch
import os

# --- Configuration ---
FAISS_INDEX_FILE = "/home/ubuntu/lagrange_lab/math_vector_db.faiss"
METADATA_FILE = "/home/ubuntu/lagrange_lab/chunk_metadata.json"
EMBEDDING_MODEL_NAME = "tbs17/MathBERT"
CACHE_DIR = "/home/ubuntu/lagrange_lab/.cache"

# --- Global Variables (Load once) ---
INDEX = None
METADATA = None
MODEL = None

def load_resources():
    """Loads the FAISS index, metadata, and embedding model into global variables."""
    global INDEX, METADATA, MODEL
    
    # Load FAISS index
    if INDEX is None:
        try:
            print(f"--- Loading FAISS index from {FAISS_INDEX_FILE} ---")
            INDEX = faiss.read_index(FAISS_INDEX_FILE)
            print(f"--- FAISS index loaded. Total entries: {INDEX.ntotal} ---")
        except Exception as e:
            print(f"Error loading FAISS index: {e}")
            INDEX = None # Ensure it's None if loading fails
            return False
            
    # Load Metadata
    if METADATA is None:
        try:
            print(f"--- Loading metadata from {METADATA_FILE} ---")
            with open(METADATA_FILE, "r", encoding="utf-8") as f:
                METADATA = json.load(f)
            if "chunks" not in METADATA or not isinstance(METADATA["chunks"], list):
                print("Error: Metadata file is missing 'chunks' list.")
                METADATA = None
                return False
            print(f"--- Metadata loaded. Number of chunks: {len(METADATA['chunks'])} ---")
        except FileNotFoundError:
            print(f"Error: Metadata file {METADATA_FILE} not found.")
            METADATA = None
            return False
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from {METADATA_FILE}.")
            METADATA = None
            return False
        except Exception as e:
            print(f"An error occurred loading metadata: {e}")
            METADATA = None
            return False
            
    # Load Embedding Model
    if MODEL is None:
        try:
            device = 'cuda' if torch.cuda.is_available() else 'cpu'
            print(f"--- Loading SentenceTransformer model: {EMBEDDING_MODEL_NAME} (Device: {device}) ---")
            MODEL = SentenceTransformer(EMBEDDING_MODEL_NAME, device=device, cache_folder=CACHE_DIR)
            print(f"--- SentenceTransformer model loaded successfully. ---")
        except Exception as e:
            print(f"Error loading SentenceTransformer model {EMBEDDING_MODEL_NAME}: {e}")
            MODEL = None
            return False
            
    # Final check
    if INDEX is not None and METADATA is not None and MODEL is not None:
        if INDEX.ntotal != len(METADATA["chunks"]):
            print(f"Error: Index size ({INDEX.ntotal}) does not match metadata size ({len(METADATA['chunks'])}). Rebuild required.")
            return False
        print("--- All resources loaded successfully. ---")
        return True
    else:
        print("--- Failed to load one or more resources. ---")
        return False

def retrieve_relevant_chunks(query, k=1):
    """Embeds a query and retrieves the top k relevant chunks."""
    if not load_resources(): # Ensure resources are loaded
        return "Error: Could not load necessary resources for retrieval."
        
    if not isinstance(query, str) or not query:
        return "Error: Invalid query provided."
        
    try:
        print(f"--- Embedding query: ", query[:100] + ("..." if len(query) > 100 else ""))
        query_embedding = MODEL.encode([query]) # Encode expects a list
        
        # Ensure query embedding is float32 and 2D
        if query_embedding.dtype != np.float32:
            query_embedding = query_embedding.astype(np.float32)
        if len(query_embedding.shape) == 1:
             query_embedding = np.expand_dims(query_embedding, axis=0)
             
        print(f"--- Query embedding generated with shape: {query_embedding.shape} ---")

        # Search the index
        print(f"--- Searching FAISS index for top {k} results... ---")
        distances, indices = INDEX.search(query_embedding, k)
        print(f"--- Search complete. Indices: {indices}, Distances: {distances} ---")
        
        # Retrieve chunks based on indices
        retrieved_chunks = []
        if indices.size > 0:
            for idx in indices[0]: # indices is 2D array [[idx1, idx2, ...]]
                if 0 <= idx < len(METADATA["chunks"]):
                    retrieved_chunks.append(METADATA["chunks"][idx])
                else:
                    print(f"Warning: Retrieved index {idx} is out of bounds.")
        
        print(f"--- Retrieved {len(retrieved_chunks)} chunks. ---")
        return "\n\n---\n\n".join(retrieved_chunks) # Join chunks with a separator
        
    except Exception as e:
        print(f"An error occurred during retrieval: {e}")
        return f"Error during retrieval: {e}"

# --- Example Usage (for testing) ---
if __name__ == "__main__":
    test_query = "How to use Lagrange multipliers for constrained optimization?"
    print(f"\n--- Testing retrieval with query: ", test_query)
    result = retrieve_relevant_chunks(test_query, k=1)
    print("\n--- Retrieval Result: ---")
    print(result)
    
    test_query_specific = "maximize x^2 + y^2 subject to x + y = 1"
    print(f"\n--- Testing retrieval with specific query: ", test_query_specific)
    result_specific = retrieve_relevant_chunks(test_query_specific, k=1)
    print("\n--- Retrieval Result (Specific): ---")
    print(result_specific)

