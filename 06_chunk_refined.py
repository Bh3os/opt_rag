import json
import re

def refine_chunks(input_file, output_file):
    """Reads marked text and splits it into chunks based on markers."""
    print(f"--- Starting chunk refinement for {input_file} ---")
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            text = f.read()
        print(f"--- Read {len(text)} characters from {input_file} ---")
    except FileNotFoundError:
        print(f"Error: Input file {input_file} not found.")
        return

    # Define the marker used for splitting
    marker = "\n--- MARKER ---\n"
    
    # Split the text by the marker
    raw_chunks = text.split(marker)
    print(f"--- Split text into {len(raw_chunks)} raw chunks based on marker ---")

    refined_chunks = []
    for i, chunk in enumerate(raw_chunks):
        # Clean up whitespace for each chunk
        cleaned_chunk = chunk.strip()
        
        # Optional: Add filtering for very small chunks if needed
        # For now, keep all non-empty chunks
        if cleaned_chunk:
            refined_chunks.append(cleaned_chunk)
            # print(f"--- Added chunk {i+1}, length {len(cleaned_chunk)} ---")
        else:
            print(f"--- Skipping empty chunk {i+1} ---")

    print(f"--- Produced {len(refined_chunks)} refined chunks ---")

    # Save chunks to a JSON file
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(refined_chunks, f, indent=2)
        print(f"--- Successfully saved refined chunks to {output_file} ---")
    except IOError as e:
        print(f"Error writing chunks to {output_file}: {e}")
    except TypeError as e:
        print(f"Error serializing chunks to JSON: {e}")

# --- Configuration ---
input_filename = "/home/ubuntu/lagrange_lab/preprocessed_math_marked_normalized.txt"
output_filename = "/home/ubuntu/lagrange_lab/refined_chunks.json"

# --- Execute Chunk Refinement ---
refine_chunks(input_filename, output_filename)

