import re

def insert_heuristic_markers_by_line(input_file, output_file, lines_per_chunk=50):
    """Reads preprocessed text and inserts markers heuristically every N lines."""
    print(f"--- Debug: Starting heuristic marker insertion by line (every {lines_per_chunk} lines) ---")
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            text = f.read()
        print(f"--- Debug: Read {len(text)} characters from {input_file} ---")
    except FileNotFoundError:
        print(f"Error: Input file {input_file} not found.")
        return

    # Split into lines
    lines = text.split("\n")
    print(f"--- Debug: Split text into {len(lines)} lines ---")

    processed_lines = []
    marker_token = "\n--- MARKER ---\n"  # Define the marker to insert (simpler newline handling)
    line_count = 0
    inserted_marker_count = 0

    for i, line in enumerate(lines):
        # Keep track of non-empty lines for the count?
        # Or just count all lines?
        # Let's count all lines for simplicity first.
        line_count += 1
        
        # Insert marker BEFORE the line if condition met (except for the very first line)
        if line_count > 1 and (line_count - 1) % lines_per_chunk == 0:
            # print(f"--- Debug: Inserting marker before line {line_count} (index {i}) ---")
            processed_lines.append(marker_token)
            inserted_marker_count += 1
        
        processed_lines.append(line)

    print(f"--- Debug: Processed {line_count} lines. Inserted {inserted_marker_count} markers. ---")

    # Join the lines back
    marked_text = "\n".join(processed_lines)
    # Clean up potential multiple blank lines - adjust regex if needed
    # marked_text = re.sub(r"(\n\s*){3,}", "\n\n", marked_text) 
    print(f"--- Debug: Final marked text length: {len(marked_text)} characters ---")

    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(marked_text.strip()) # Write the text with markers
        print(f"--- Debug: Successfully wrote marked text to {output_file} ---")
        print(f"Inserted heuristic markers every {lines_per_chunk} lines. Saved to {output_file}")
    except IOError as e:
        print(f"Error writing marked text to {output_file}: {e}")

# --- Configuration ---
input_filename = "/home/ubuntu/lagrange_lab/preprocessed_math_headers.txt"
output_filename = "/home/ubuntu/lagrange_lab/preprocessed_math_marked.txt"
# Insert a marker roughly every 50 lines as a heuristic
lines_per_chunk_heuristic = 50

# --- Execute Marker Insertion ---
insert_heuristic_markers_by_line(input_filename, output_filename, lines_per_chunk_heuristic)

