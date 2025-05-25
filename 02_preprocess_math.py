import re

# Change function definition parameters
def preprocess_math_text(input_filename, output_filename):
    try:
        # Use the correct parameter name here
        with open(input_filename, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
    except FileNotFoundError:
        # Use the correct parameter name here
        print(f"Error: Input file {input_filename} not found.")
        return

    # --- Typo Corrections (Simplified for debugging) ---
    # The original dictionary is causing syntax errors. Using a minimal version.
    corrections = {
        r'Dimltri': 'Dimitri',
        r'hlassachusetts': 'Massachusetts',
        r'pamllel': 'parallel',
        r'coinputation': 'computation',
        r'\blambda1': 'lambda^T',
        r'\blambda\'': 'lambda^T',
        # Add more simple, known-good corrections if needed
    }
    
    # --- Original Large Dictionary (Commented Out) ---
    """
    corrections = {
        # General Typos & OCR Errors
        r'Dimltri': 'Dimitri',
        r'hlassachusetts': 'Massachusetts',
        r'pamllel': 'parallel',
        # ... (rest of the large dictionary) ...
        r' \n': '\n',
    }
    """

    processed_text = text
    print("--- Applying simplified corrections ---")
    for pattern, replacement in corrections.items():
        try:
            processed_text = re.sub(pattern, replacement, processed_text, flags=re.IGNORECASE)
        except re.error as e:
            print(f"Regex error for pattern '{pattern}': {e}")
            continue
    print("--- Finished applying simplified corrections ---")

    # --- Remove non-math sections (heuristic) ---
    print("--- Removing non-math sections (References, Bibliography, Index) ---")
    processed_text = re.sub(r'\nReferences\n.*', '', processed_text, flags=re.DOTALL | re.IGNORECASE)
    processed_text = re.sub(r'\nBibliography\n.*', '', processed_text, flags=re.DOTALL | re.IGNORECASE)
    processed_text = re.sub(r'\nIndex\n.*', '', processed_text, flags=re.DOTALL | re.IGNORECASE)
    print("--- Finished removing non-math sections ---")

    # --- Final whitespace cleanup ---
    print("--- Performing final whitespace cleanup ---")
    processed_text = re.sub(r'\n\s*\n', '\n\n', processed_text) # Consolidate blank lines
    processed_text = processed_text.strip()
    print("--- Finished final whitespace cleanup ---")

    try:
        # Use the correct parameter name here
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(processed_text)
        # Use the correct parameter name here
        print(f"Preprocessed math text saved to {output_filename}")
    except IOError as e:
        # Use the correct parameter name here
        print(f"Error writing to output file {output_filename}: {e}")

# Define input and output file paths
input_filename = "/home/ubuntu/lagrange_lab/cleaned_layout_text.txt"
output_filename = "/home/ubuntu/lagrange_lab/preprocessed_math.txt"

# Run the preprocessing function with correct variable names
print(f"--- Starting preprocessing script for {input_filename} -> {output_filename} ---")
preprocess_math_text(input_filename, output_filename)
print("--- Preprocessing script finished ---")

