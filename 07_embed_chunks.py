import json
from sentence_transformers import SentenceTransformer
import numpy as np
import torch # Check if GPU is available

def embed_chunks(chunk_file, model_name, output_file):
    """Loads chunks, embeds them using a SentenceTransformer model, and saves embeddings."""
    print(f"--- Starting embedding process for {chunk_file} using {model_name} ---")
    
    # Load chunks
    try:
        with open(chunk_file, 'r', encoding='utf-8') as f:
            chunks = json.load(f)
        print(f"--- Loaded {len(chunks)} chunks from {chunk_file} ---")
        if not chunks:
            print("Error: No chunks found in the input file.")
            return
        # Ensure chunks are strings
        if not all(isinstance(chunk, str) for chunk in chunks):
            print("Error: Input file does not contain a list of strings.")
            return
            
    except FileNotFoundError:
        print(f"Error: Chunk file {chunk_file} not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {chunk_file}.")
        return
    except Exception as e:
        print(f"An error occurred loading chunks: {e}")
        return

    # Initialize model
    try:
        # Check for GPU availability
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f"--- Using device: {device} ---")
        # Specify cache directory within the project folder to avoid potential permission issues
        cache_dir = "/home/ubuntu/lagrange_lab/.cache"
        model = SentenceTransformer(model_name, device=device, cache_folder=cache_dir)
        print(f"--- Loaded SentenceTransformer model: {model_name} --- (Cache: {cache_dir})")
    except Exception as e:
        print(f"Error loading SentenceTransformer model {model_name}: {e}")
        return

    # Generate embeddings
    try:
        print(f"--- Generating embeddings for {len(chunks)} chunks... ---")
        # The encode method handles batching internally if needed
        embeddings = model.encode(chunks, show_progress_bar=True)
        print(f"--- Generated embeddings with shape: {embeddings.shape} ---")
        
        # Ensure embeddings are numpy array
        if not isinstance(embeddings, np.ndarray):
             embeddings = np.array(embeddings)
             print(f"--- Converted embeddings to NumPy array, shape: {embeddings.shape} ---")

    except Exception as e:
        print(f"Error generating embeddings: {e}")
        return

    # Save embeddings
    try:
        np.save(output_file, embeddings)
        print(f"--- Successfully saved embeddings to {output_file} ---")
    except IOError as e:
        print(f"Error saving embeddings to {output_file}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred saving embeddings: {e}")

# --- Configuration ---
chunk_filename = "/home/ubuntu/lagrange_lab/refined_chunks.json"
embedding_model_name = "tbs17/MathBERT"
output_embeddings_file = "/home/ubuntu/lagrange_lab/mathbert_embeddings.npy"

# --- Execute Embedding ---
embed_chunks(chunk_filename, embedding_model_name, output_embeddings_file)

