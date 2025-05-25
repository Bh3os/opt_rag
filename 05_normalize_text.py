import re
import os
import sys

def normalize_text_file(input_file, output_file):
    """Reads a text file, normalizes line endings to \n, and removes excessive whitespace."""
    print(f"--- Starting normalization for {input_file} ---")
    try:
        # Read the file in binary mode to detect different line endings
        with open(input_file, "rb") as f:
            content_bytes = f.read()
        print(f"--- Read {len(content_bytes)} bytes from {input_file} ---")
        
        # Decode assuming UTF-8, replace errors
        content = content_bytes.decode("utf-8", errors="replace")
        
        # Normalize line endings: replace \r\n and \r with \n
        normalized_content = content.replace("\r\n", "\n").replace("\r", "\n")
        print(f"--- Normalized line endings (replaced \\r\\n and \\r with \\n) ---")
        
        # Optional: Remove leading/trailing whitespace from each line
        lines = normalized_content.split("\n")
        stripped_lines = [line.strip() for line in lines]
        print(f"--- Stripped leading/trailing whitespace from {len(lines)} lines ---")
        
        # Optional: Remove excessive blank lines (more than two consecutive)
        normalized_content = "\n".join(stripped_lines)
        normalized_content = re.sub(r"\n{3,}", "\n\n", normalized_content)
        print(f"--- Removed excessive blank lines (kept max 2 consecutive) ---")

        # Count lines in the final normalized text
        final_lines = normalized_content.split("\n")
        print(f"--- Final normalized text has {len(final_lines)} lines ---")

        # Write the normalized content back to the output file
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(normalized_content.strip()) # Use strip() to remove potential leading/trailing whitespace from the whole text
        print(f"--- Successfully wrote normalized text to {output_file} ---")
        
    except FileNotFoundError:
        print(f"Error: Input file {input_file} not found.")
    except Exception as e:
        print(f"An error occurred during normalization: {e}")

# --- Configuration ---
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python normalize_text.py <input_file> <output_file>")
        sys.exit(1)
    
    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

    # --- Execute Normalization ---
    normalize_text_file(input_filename, output_filename)

