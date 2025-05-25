**Lagrange Optimization Lab: RAG Pipeline Report**

**1. Introduction**
This report details the construction and functionality of the "Lagrange Optimization Lab," a Retrieval-Augmented Generation (RAG) pipeline designed to solve constrained optimization problems using the method of Lagrange multipliers. The pipeline leverages mathematical text from provided textbooks, embeds relevant content using MathBERT, retrieves pertinent information based on user queries, and employs a symbolic solver (SymPy) to find solutions.

**2. Pipeline Stages**

*   **Retrieval Stage:**
    *   **Source Processing:** Text was extracted from the provided PDF textbooks ("Constrained Optimization and Lagrange Multiplier Methods" by Bertsekas and "Lagrange multiplier approach to variational problems and applications" by Ito & Kunisch) using `pdftotext` with layout preservation.
    *   **Preprocessing & Cleaning:** The extracted text underwent cleaning to remove headers/footers, fix common OCR errors, and standardize basic mathematical notation (though the full correction dictionary was simplified due to syntax issues). Whitespace and line endings were normalized.
    *   **Chunking:** The preprocessed text was segmented into meaningful chunks using synthetic headers (based on keywords like "Lagrange Multiplier Methods") and heuristic line counts as markers.
    *   **Embedding:** The text chunks were embedded using the `tbs17/MathBERT` model (768 dimensions) via the `sentence-transformers` library.
    *   **Vector Database:** A FAISS `IndexFlatL2` vector database was created to store the MathBERT embeddings, enabling efficient semantic similarity search. Chunk text was stored separately as metadata.
    *   **Retrieval Logic:** A retrieval function was implemented to take a natural language query (e.g., "maximize x^2 + y^2 given x + y = 1"), embed it using MathBERT, and search the FAISS index to find the most relevant text chunk(s) based on vector similarity (L2 distance).

*   **Generation Stage:**
    *   **Query Parsing:** The user's optimization problem query is parsed to identify the objective function, constraint equation(s), and variables.
    *   **Lagrangian Formulation:** Using the SymPy library, the Lagrangian function L = f - λ(g - c) is constructed symbolically based on the parsed objective (f) and constraint (g=c).
    *   **Symbolic Differentiation:** Partial derivatives of the Lagrangian with respect to each variable and the Lagrange multiplier (λ) are computed (∇L).
    *   **System Solving:** The system of equations formed by setting the partial derivatives to zero (∇L = 0) is solved symbolically using `sympy.solve()` to find potential critical points (values for variables and λ).

*   **Integration Stage:**
    *   **Solution Evaluation:** The objective function is evaluated at the critical points found by the solver.
    *   **Result Summarization:** The final solution, including the critical point(s), the value of the objective function at those points, and the value of the Lagrange multiplier(s), is compiled. The Lagrangian and the system of equations solved are also included for transparency.
    *   **Visualization:** For 2D problems, a Chart.js scatter plot is generated to visualize the constraint line and the location of the critical point. (The code for the test case is provided below).

**3. Chart.js Visualization Code (for f(x, y) = x^2 + y^2 subject to x + y = 1)**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lagrange Optimization Visualization</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-annotation"></script>
    <style>
        body { font-family: sans-serif; padding: 20px; }
        .chart-container { position: relative; height: 400px; width: 400px; margin: auto; }
    </style>
</head>
<body>

<h2>Visualization for f(x, y) = x^2 + y^2 subject to x + y = 1</h2>
<div class="chart-container">
    <canvas id="optimizationChart"></canvas>
</div>

<script>
    const ctx = document.getElementById("optimizationChart").getContext("2d");

    // Data for the constraint line x + y = 1 (or y = 1 - x)
    const constraintLineData = [];
    for (let x = -2; x <= 3; x += 0.5) {
        constraintLineData.push({ x: x, y: 1 - x });
    }

    // Critical point found by Lagrange solver
    const criticalPoint = { x: 0.5, y: 0.5 }; // From solver output

    const chart = new Chart(ctx, {
        type: "scatter",
        data: {
            datasets: [
                {
                    label: "Constraint Line (x + y = 1)",
                    data: constraintLineData,
                    borderColor: "blue",
                    borderWidth: 1,
                    pointRadius: 0,
                    showLine: true,
                    fill: false,
                    tension: 0 // Ensure straight lines for linear constraint
                },
                {
                    label: "Critical Point (0.5, 0.5)",
                    data: [criticalPoint],
                    backgroundColor: "red",
                    pointRadius: 5,
                    pointHoverRadius: 7
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                x: {
                    type: "linear",
                    position: "bottom",
                    title: {
                        display: true,
                        text: "x"
                    },
                    min: -2,
                    max: 3
                },
                y: {
                    title: {
                        display: true,
                        text: "y"
                    },
                    min: -2,
                    max: 3
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: "Lagrange Multiplier Critical Point"
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            let label = context.dataset.label || 		;
                            if (label) {
                                label += 	: 	;
                            }
                            if (context.parsed.x !== null) {
                                label += `(${context.parsed.x}, ${context.parsed.y})`;
                            }
                            // Add f value for the critical point
                            if (context.dataset.label === "Critical Point (0.5, 0.5)") {
                                label += ` - f(x,y) = ${criticalPoint.x**2 + criticalPoint.y**2}`;
                            }
                            return label;
                        }
                    }
                }
            }
        }
    });
</script>

</body>
</html>
```

**4. Data Flow Summary**
User Query (e.g., "maximize x^2+y^2 s.t. x+y=1") → Query Embedding (MathBERT) → FAISS Search → Retrieve Relevant Chunks → (Context for LLM - *Note: LLM integration not implemented in this version*) → Parse Query → Symbolic Solver (SymPy: Lagrangian, Derivatives, Solve) → Extract Solution (Critical Point, f-value, λ) → Generate Visualization (Chart.js) & Summary → Final Output.

**Note on LLM Integration:** The provided OpenRouter API key and LLM details were noted but not integrated into this version of the pipeline, which focuses on symbolic solving based on the retrieved context (though the retrieval context isn't directly used by the current solver). A future version could use the retrieved chunks to guide an LLM in formulating or interpreting the problem/solution.

**Note on Preprocessing:** The text preprocessing encountered challenges, particularly with the large corrections dictionary causing syntax errors. A simplified version was used to ensure pipeline functionality. The quality of retrieval depends heavily on the quality of text extraction, cleaning, and chunking. The current retrieval returns the same chunk for both test queries, indicating the small number of chunks (4) limits retrieval specificity. More robust preprocessing and finer-grained chunking would improve results.

**Deliverables:**
The following key files are attached:
*   `report.md`: This summary report.
*   `lagrange_solver.py`: Python script for the symbolic solver.
*   `retrieve_chunks.py`: Python script for the retrieval logic.
*   `visualization.html`: HTML file with the Chart.js visualization for the test case.
*   `math_vector_db.faiss`: The FAISS index file.
*   `chunk_metadata.json`: JSON file containing the text chunks.
*   `mathbert_embeddings.npy`: NumPy file with the chunk embeddings.
*   `preprocess_math.py`: Python script for preprocessing (simplified).
*   `chunk_refined.py`: Python script for chunking.
*   `build_vector_db.py`: Python script for building the FAISS index.
*   `embed_chunks.py`: Python script for embedding chunks.

