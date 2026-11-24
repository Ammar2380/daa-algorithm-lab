# DAA Algorithm Lab

A Design and Analysis of Algorithms (DAA) semester project built with Python and Streamlit.

The project contains 16 algorithms from six different topics. Each algorithm is implemented manually and can be explored through step-by-step visualizations.

## Algorithms

| Category | Algorithms |
|---|---|
| Searching | Linear Search, Binary Search |
| Sorting | Insertion Sort, Merge Sort, Quick Sort, Heap Sort |
| Divide and Conquer | Strassen's Matrix Multiplication |
| Dynamic Programming | Matrix Chain Multiplication, LCS |
| Greedy | Activity Selection, Fractional Knapsack, Huffman Coding |
| Graph | BFS, DFS, Dijkstra, Kruskal |

The algorithms are implemented without using built-in functions for sorting, searching, shortest paths, MST, or dynamic programming.

## Requirements

- Python 3.11+
- VS Code (recommended)
- pip

## Setup

Open the project folder in VS Code and open a terminal.

### 1. Create a virtual environment

```bash
python -m venv venv
```

### 2. Activate the environment

**Windows PowerShell:**

```bash
venv\Scripts\activate
```

If PowerShell blocks the command, run:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Then activate the environment again.

**Mac/Linux:**

```bash
source venv/bin/activate
```

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the application

```bash
streamlit run app.py
```

The application will be available at:

```text
http://localhost:8501
```

## Project Structure

```text
app.py
    Main dashboard and navigation

views/
    Streamlit pages for each algorithm category
    Performance Analyzer

algorithms/
    Algorithm implementations
    data_structures.py
        MinHeap
        UnionFind
        merge_sort_by

core/
    step_tracker.py
    complexity.py
    algorithm_registry.py
    benchmark.py
    validation.py

visualizations/
    Algorithm visualizers
    Shared UI components
    Charts and theme

data/
    sample_graphs.json

tests/
    Project test suite

docs/
    algorithm_reference.md
    project_report.md
    benchmark_results.md

scripts/
    generate_reference.py
    run_benchmarks.py

assets/
    style.css
```

## How the Application Works

Each algorithm can run normally or with a `StepTracker`.

When the tracker is enabled, the algorithm records important steps such as comparisons, swaps, selections, and other operations. These steps are then shown in the visualizer.

The algorithm itself does not depend on Streamlit. When the tracker is not used, the algorithm runs normally without storing visualization steps.

## Algorithm Pages

Each category has its own page.

The pages include:

- Algorithm explanation
- Problem description
- Pseudocode
- Time complexity
- Space complexity
- Python implementation
- Example
- Interactive visualizer

The visualizers support:

- Reset
- Previous step
- Next step
- Play / Resume
- Pause
- Step slider

Input can be entered manually or generated randomly.

Invalid input is handled with an error message instead of crashing the application.

## Performance Analyzer

The Performance Analyzer can be used to compare the running time of the implemented algorithms.

You can select:

- Algorithm category
- Input scenario
- Input sizes
- Number of repetitions

The analyzer displays:

- Execution time
- Operation counts
- Results table
- Optional theoretical complexity curves
- CSV export

Benchmark results are measured on the machine running the application.

## Design

The project uses a shared design system.

The main colors are defined in:

```text
visualizations/theme.py
```

The stylesheet is located at:

```text
assets/style.css
```

Common UI elements are implemented in:

```text
visualizations/layout.py
visualizations/ui_components.py
```

This keeps the pages consistent and avoids repeating the same UI code.

## Some Implementation Details

### Binary Search

Binary Search requires sorted data. The application checks the input and provides an option to sort it before searching.

### Strassen's Matrix Multiplication

Strassen's algorithm works with matrices whose dimensions are powers of two. The implementation pads other matrix sizes with zeros and removes the extra rows and columns from the final result.

### Quick Sort

Quick Sort uses an explicit stack instead of recursive calls. This avoids hitting Python's recursion limit when processing inputs that produce a worst-case partitioning pattern.

### Benchmarks

The benchmark system runs the algorithms multiple times and uses the measured results to compare their performance.

## Running Tests

The project uses pytest.

Run:

```bash
pytest -q
```

The test suite covers:

- Algorithm correctness
- Edge cases
- Input validation
- Operation tracking
- Benchmarking
- UI pages
- Algorithm options
- Visualizer steps

## Project Goals

The main goals of the project are to:

1. Implement common DAA algorithms from scratch.
2. Show how the algorithms work through visualizations.
3. Compare their theoretical and practical performance.
4. Provide a simple interface for experimenting with different inputs.
5. Apply the concepts covered in the DAA course in one project.

## Built With

- Python
- Streamlit
- Plotly
- NumPy
- pytest

## Course

**Design and Analysis of Algorithms (DAA)**

Semester Project