import re

def insert_synthetic_headers(input_file, output_file):
    """Reads preprocessed text and inserts synthetic Markdown headers based on patterns."""
    print(f"--- Starting header insertion for {input_file} ---")
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            text = f.read()
        print(f"--- Read {len(text)} characters from {input_file} ---")
    except FileNotFoundError:
        print(f"Error: Input file {input_file} not found.")
        return

    # Define patterns for potential section starts
    # More specific patterns first
    header_patterns = {
        # Matches things like "Theorem 3.1", "Proposition 4.2", "Lemma 2.A"
        r"^((?:Theorem|Proposition|Lemma|Corollary|Definition|Remark|Example)\s+[\d\w\.]+)[:.\s]*$": r"### \1",
        # Matches chapter/section headers like "Chapter 1", "Section 2.3"
        r"^((?:Chapter|Section)\s+[\d\.]+)[:.\s]*$": r"## \1",
        # Matches specific keywords indicating important concepts
        r"^(Lagrange Multiplier Method[s]?)": r"### \1",
        r"^(Augmented Lagrangian Method[s]?)": r"### \1",
        r"^(Penalty Method[s]?)": r"### \1",
        r"^(Karush.Kuhn.Tucker|KKT)\s+Conditions?": r"### Karush-Kuhn-Tucker (KKT) Conditions",
        r"^(Optimality Condition[s]?)": r"### Optimality Conditions",
        r"^(Duality Theory)": r"### Duality Theory",
        r"^(Sensitivity Analysis)": r"### Sensitivity Analysis",
        # Add more patterns as needed
    }

    lines = text.split("\n")
    processed_lines = []
    inserted_headers = 0

    for line in lines:
        processed_line = line
        # Check each pattern against the start of the line (case-insensitive)
        for pattern, header_format in header_patterns.items():
            match = re.match(pattern, line.strip(), re.IGNORECASE)
            if match:
                # Extract the matched text (group 1 if defined, else full match)
                header_text = match.group(1) if match.groups() else match.group(0)
                # Format the header
                synthetic_header = header_format.replace("\\1", header_text.strip())
                # Insert header *before* the matched line
                processed_lines.append("\n" + synthetic_header)
                inserted_headers += 1
                # print(f"--- Inserted header: {synthetic_header} for line: {line[:50]}... ---")
                break # Stop checking patterns for this line once one matches
        
        processed_lines.append(processed_line)

    print(f"--- Inserted {inserted_headers} synthetic headers ---")
    processed_text = "\n".join(processed_lines)
    
    # Clean up extra newlines potentially introduced
    processed_text = re.sub(r"\n{3,}", "\n\n", processed_text)

    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(processed_text.strip())
        print(f"--- Successfully wrote text with synthetic headers to {output_file} ---")
    except IOError as e:
        print(f"Error writing to output file {output_file}: {e}")

# --- Configuration ---
input_filename = "/home/ubuntu/lagrange_lab/preprocessed_math.txt"
output_filename = "/home/ubuntu/lagrange_lab/preprocessed_math_headers.txt"

# --- Execute Header Insertion ---
insert_synthetic_headers(input_filename, output_filename)

