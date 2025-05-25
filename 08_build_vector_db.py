import json
import numpy as np
import faiss
import os

def build_faiss_index(embeddings_file, chunk_file, index_file, metadata_file):
    """Loads embeddings and chunks, builds a FAISS index, and saves index and metadata."""
    print(f"--- Starting FAISS index construction from {embeddings_file} and {chunk_file} ---")

    # Load embeddings
    try:
        embeddings = np.load(embeddings_file)
        # Ensure embeddings are float32, as required by FAISS
        if embeddings.dtype != np.float32:
            print(f"--- Converting embeddings from {embeddings.dtype} to float32 ---")
            embeddings = embeddings.astype(np.float32)
        print(f"--- Loaded embeddings with shape: {embeddings.shape} and dtype: {embeddings.dtype} ---")
        if len(embeddings.shape) != 2:
            print("Error: Embeddings file does not contain a 2D numpy array.")
            return
        dimension = embeddings.shape[1]
        num_embeddings = embeddings.shape[0]
        print(f"--- Embedding dimension: {dimension}, Number of embeddings: {num_embeddings} ---")
    except FileNotFoundError:
        print(f"Error: Embeddings file {embeddings_file} not found.")
        return
    except Exception as e:
        print(f"Error loading embeddings: {e}")
        return

    # Load chunks (metadata)
    try:
        with open(chunk_file, 'r', encoding='utf-8') as f:
            chunks = json.load(f)
        print(f"--- Loaded {len(chunks)} chunks from {chunk_file} ---")
        if len(chunks) != num_embeddings:
            print(f"Error: Number of chunks ({len(chunks)}) does not match number of embeddings ({num_embeddings}).")
            return
        # Store chunks as metadata (simple list for now)
        metadata = {"chunks": chunks}
    except FileNotFoundError:
        print(f"Error: Chunk file {chunk_file} not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {chunk_file}.")
        return
    except Exception as e:
        print(f"An error occurred loading chunks: {e}")
        return

    # Build FAISS index
    try:
        print(f"--- Building FAISS IndexFlatL2 with dimension {dimension} ---")
        # Using IndexFlatL2 for exact search, suitable for small datasets
        index = faiss.IndexFlatL2(dimension)
        print(f"--- FAISS index created. Is trained: {index.is_trained} ---")
        print(f"--- Adding {num_embeddings} embeddings to the index... ---")
        index.add(embeddings)
        print(f"--- Embeddings added. Index total entries: {index.ntotal} ---")
    except Exception as e:
        print(f"Error building FAISS index: {e}")
        return

    # Save index and metadata
    try:
        print(f"--- Saving FAISS index to {index_file} ---")
        faiss.write_index(index, index_file)
        print(f"--- FAISS index saved successfully. ---")
    except Exception as e:
        print(f"Error saving FAISS index: {e}")
        return
        
    try:
        print(f"--- Saving chunk metadata to {metadata_file} ---")
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
        print(f"--- Chunk metadata saved successfully. ---")
    except IOError as e:
        print(f"Error saving metadata to {metadata_file}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred saving metadata: {e}")

# --- Configuration ---
embeddings_filename = "/home/ubuntu/lagrange_lab/mathbert_embeddings.npy"
chunk_filename = "/home/ubuntu/lagrange_lab/refined_chunks.json"
faiss_index_filename = "/home/ubuntu/lagrange_lab/math_vector_db.faiss"
metadata_filename = "/home/ubuntu/lagrange_lab/chunk_metadata.json"

# --- Execute Index Building ---
build_faiss_index(embeddings_filename, chunk_filename, faiss_index_filename, metadata_filename)

