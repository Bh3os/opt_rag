import re
import os

def clean_layout_text(input_files, output_file):
    """Cleans text extracted with pdftotext -layout, removing artifacts and combining files."""
    print(f"--- Starting cleaning for layout text: {input_files} ---")
    full_cleaned_text = ""

    for input_file in input_files:
        try:
            with open(input_file, "r", encoding="utf-8") as f:
                text = f.read()
            print(f"--- Read {len(text)} characters from {input_file} ---")

            # Remove form feed characters
            cleaned_text = text.replace("\f", "\n") # Replace form feed with newline
            print(f"--- Replaced form feed characters ---")

            # Normalize whitespace: replace multiple spaces/tabs with a single space
            cleaned_text = re.sub(r"[ \t]+", " ", cleaned_text)
            print(f"--- Normalized spaces/tabs ---")

            # Attempt to remove excessive blank lines (more than 2 consecutive)
            lines = cleaned_text.split("\n")
            # Keep lines with content or single blank lines for paragraph separation
            filtered_lines = []
            blank_line_count = 0
            for line in lines:
                stripped_line = line.strip()
                if stripped_line:
                    filtered_lines.append(stripped_line)
                    blank_line_count = 0
                elif blank_line_count < 2: # Allow up to two blank lines
                    filtered_lines.append("") # Keep the blank line marker
                    blank_line_count += 1
            
            cleaned_text = "\n".join(filtered_lines)
            print(f"--- Removed excessive blank lines (kept max 2) ---")

            # Basic filtering (can be expanded based on inspection)
            # Remove lines that seem like page numbers (e.g., just digits at start/end of line)
            cleaned_text = re.sub(r"^\d+\n", "", cleaned_text, flags=re.MULTILINE)
            cleaned_text = re.sub(r"\n\d+$", "", cleaned_text, flags=re.MULTILINE)
            print(f"--- Attempted removal of simple page numbers ---")

            # Add cleaned text from this file to the combined output
            full_cleaned_text += cleaned_text + "\n\n--- END OF FILE: {} ---\n\n".format(os.path.basename(input_file))

        except FileNotFoundError:
            print(f"Error: Input file {input_file} not found.")
        except Exception as e:
            print(f"An error occurred during cleaning {input_file}: {e}")

    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(full_cleaned_text.strip())
        print(f"--- Successfully wrote combined cleaned text to {output_file} ---")
    except IOError as e:
        print(f"Error writing cleaned text to {output_file}: {e}")

# --- Configuration ---
input_filenames = [
    "/home/ubuntu/lagrange_lab/bertsekas_layout.txt",
    "/home/ubuntu/lagrange_lab/ito_kunisch_layout.txt"
]
output_filename = "/home/ubuntu/lagrange_lab/cleaned_layout_text.txt"

# --- Execute Cleaning ---
clean_layout_text(input_filenames, output_filename)

