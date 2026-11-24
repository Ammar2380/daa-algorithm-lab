# DAA Algorithm Lab: Interactive Algorithm Visualizer and Performance Analyzer

## 1. Title Page

| | |
|---|---|
| **Project title** | DAA Algorithm Lab: Interactive Algorithm Visualizer and Performance Analyzer |
| **Course** | Design and Analysis of Algorithms |
| **Submitted by** | *(your name, roll number)* |
| **Supervisor** | *(instructor name)* |
| **Department / University** | *(department, university)* |
| **Date** | *(submission date)* |

## 2. Abstract
This project is an educational web application, written in Python with Streamlit, that teaches 16 classic algorithms from a Design and Analysis of Algorithms course. Each algorithm is implemented by hand and can be run on user-supplied input, watched step by step, and studied through pseudocode, complexity analysis and real source code. A Performance Analyzer measures execution time and counts operations on identical inputs, and compares the results with theoretical complexity. The algorithms are verified by an automated test suite of 193 tests (including brute-force cross-checks). Measured results show the theory clearly (for example Insertion Sort growing quadratically and Binary Search staying almost flat) and also show where practice differs from theory (Strassen's algorithm uses fewer multiplications yet is slower in Python at the tested sizes).

## 3. Introduction
Algorithms are usually taught with pseudocode and paper traces, which makes it hard to see *why* an algorithm behaves as it does. Visualization and measurement turn abstract complexity classes such as O(n log n) into things a student can observe. This project provides a single tool covering searching, sorting, divide and conquer, dynamic programming, greedy algorithms and graph algorithms.

## 4. Problem Statement
Students struggle to connect algorithm theory with behaviour. Existing tools are often static images, cover only a few algorithms, or hide the implementation behind library calls. The problem is to build one interactive, correct and well-documented tool that shows how algorithms execute, explains their complexity, and compares their real performance.

## 5. Project Objectives
1. Implement 16 algorithms manually, without built-in substitutes.
2. Let users run each algorithm on their own input with graceful handling of invalid input.
3. Visualize execution step by step with Reset, Previous, Next, Play/Resume and Pause controls.
4. Present pseudocode, best/average/worst time and auxiliary space for each algorithm.
5. Benchmark algorithms fairly and compare measured with theoretical complexity.
6. Verify correctness with automated tests.

## 6. Scope of the Project
**In scope:** the 16 algorithms below, step-by-step visualization, performance analysis, documentation, tests.
**Out of scope:** user accounts, saving sessions, directed-graph editing in the UI, parallel algorithms, and algorithms outside the list. Visualization is limited to small inputs (arrays up to 40 items, matrices up to 8x8, strings up to 12 characters for DP tables, graphs up to 20 vertices) to stay readable; the Performance Analyzer handles much larger inputs.

| Category | Algorithms |
|---|---|
| Searching | Linear Search, Binary Search |
| Sorting | Insertion, Merge, Quick, Heap Sort |
| Divide and Conquer | Strassen's Matrix Multiplication |
| Dynamic Programming | Matrix Chain Multiplication, Longest Common Subsequence |
| Greedy | Activity Selection, Fractional Knapsack, Huffman Coding |
| Graph | BFS, DFS, Dijkstra, Kruskal |

(The original brief said "15 algorithms" but listed 16; all 16 are implemented.)

## 7. Proposed Methodology
Development followed eight phases: (1) project set-up and dashboard, (2) searching and sorting, (3) Strassen, (4) dynamic programming, (5) greedy, (6) graph, (7) performance analyzer, (8) testing, documentation and report. For each algorithm the sequence was: study the theory, implement in a UI-independent module, write tests (including brute-force comparison), add step recording, build the visualization, then document.

**Step recording.** Every algorithm takes an optional `StepTracker`. When supplied, it stores snapshots with a text explanation; when omitted a do-nothing tracker is used so normal runs are not slowed.

**Fair benchmarking.** For each input size one dataset is generated from a fixed random seed and given to every algorithm; each algorithm is timed several times and the median is reported; operation counts come from a separate instrumented run so they do not disturb timing.

## 8. System Architecture
The system has three layers.

| Layer | Folders | Responsibility |
|---|---|---|
| Logic | `algorithms/`, `core/` | Algorithms, step tracking, validation, benchmarking, documentation data. No Streamlit code. |
| Visualization | `visualizations/` | Turns recorded steps into Plotly / Matplotlib figures and styled tables; shared Streamlit widgets. |
| Interface | `app.py`, `views/` | Dashboard and one page per category plus the Performance Analyzer. |

Key files: `core/step_tracker.py` (counters and snapshots), `core/complexity.py` (single source for all documentation, used by both the app and `docs/algorithm_reference.md`), `core/benchmark.py` (benchmark suites), `core/validation.py` (input parsing), `algorithms/data_structures.py` (hand-written min-heap, union-find and key-based merge sort), `visualizations/ui_components.py` (algorithm information tabs and the step player).

Data flow: user input -> `validation` -> algorithm (with a `StepTracker`) -> list of steps -> visualization function -> displayed by the step player.

## 9. Algorithm Explanations, 10. Pseudocode and 11. Time and Space Complexity
Full explanations, pseudocode and complexity for all 16 algorithms (problem, input/output, steps, pseudocode, best/average/worst time, auxiliary space, applications, example) are in **`docs/algorithm_reference.md`** (generated from the same data the application displays, so the two always agree). Summary:

| Algorithm | Best | Average | Worst | Space |
|---|---|---|---|---|
| Linear Search | O(1) | O(n) | O(n) | O(1) |
| Binary Search | O(1) | O(log n) | O(log n) | O(1) |
| Insertion Sort | O(n) | O(n^2) | O(n^2) | O(1) |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) |
| Quick Sort | O(n log n) | O(n log n) | O(n^2) | O(log n) average; O(n) worst case in this implementation |
| Heap Sort | O(n log n) | O(n log n) | O(n log n) | O(1) |
| Strassen's Matrix Multiplication | Theta(n^log2(7)) ~ Theta(n^2.81) | Theta(n^2.81) | Theta(n^2.81) | O(n^2) |
| Matrix Chain Multiplication | Theta(n^3) | Theta(n^3) | Theta(n^3) | Theta(n^2) |
| Longest Common Subsequence (LCS) | Theta(mn) | Theta(mn) | Theta(mn) | Theta(mn) |
| Activity Selection | O(n log n) | O(n log n) | O(n log n) | O(n) |
| Fractional Knapsack | O(n log n) | O(n log n) | O(n log n) | O(n) |
| Huffman Coding | O(n) | O(n + k log k) | O(n + k log k), k = number of distinct characters | O(k) |
| Breadth-First Search (BFS) | O(V + E) | O(V + E) | O(V + E) | O(V) |
| Depth-First Search (DFS) | O(V + E) | O(V + E) | O(V + E) | O(V) |
| Dijkstra's Shortest Path | O((V + E) log V) | O((V + E) log V) | O((V + E) log V) | O(V + E) |
| Kruskal's Minimum Spanning Tree | O(E log E) | O(E log E) | O(E log E) = O(E log V) | O(V + E) |

Notes on the less obvious entries:
* **Quick Sort** worst case is O(n^2) because the last element is the pivot; sorted input triggers it. Measured: 499,500 comparisons for n = 1000 (= n(n-1)/2).
* **Strassen**: T(n) = 7T(n/2) + Theta(n^2) gives Theta(n^(log2 7)) = Theta(n^2.81) by the Master theorem.
* **Huffman**: O(n) to count frequencies plus O(k log k) for k-1 heap merges, k = number of distinct characters.
* **Dijkstra** (binary heap, lazy deletion): O((V+E) log V). **Kruskal**: O(E log E), dominated by sorting.
* **DP algorithms** fill every table cell exactly once, so the best, average and worst cases coincide.

## 12. Implementation Details
* **Language and libraries:** Python 3.11+, Streamlit (interface), Plotly and Matplotlib (figures), NetworkX (graph layout), NumPy (matrix storage and quadrant slicing), pandas (tables), pytest (tests).
* **No substitutes:** sorting, searching, shortest path, MST and DP are all written by hand. NumPy is used only to hold matrices and slice quadrants; the Strassen recurrence and the classical triple loop are written explicitly. The heap and union-find structures are also hand-written.
* **Strassen and non-power-of-two sizes:** matrices are padded with zeros to the next power of two, multiplied, and the result is cut back to the original size.
* **Quick Sort** uses an explicit stack so worst-case inputs cannot exceed Python's recursion limit. **DFS** also uses an explicit stack but produces the same order as the recursive version.
* **Binary Search** does not check sortedness itself (that would cost O(n) and hide its O(log n) behaviour); the page checks, warns and offers to sort first.
* **Step player:** buttons change a slider value held in Streamlit session state. *Play* iterates through the remaining steps; pressing *Pause* (or any widget) interrupts the run and the position is kept, so *Play / Resume* continues from there.
* **User interface:** a single design system (palette in `visualizations/theme.py`, stylesheet in `assets/style.css`, reusable components in `visualizations/layout.py`) gives every page the same dark, responsive look. Navigation is declared once with `st.navigation`; pages live in `views/`.
* **Input safety:** all typed input goes through `core/validation.py`; algorithms raise `ValueError` or `TypeError` for invalid data and pages turn these into messages.

## 13. Screenshots
*Insert your own screenshots here (run `streamlit run app.py`, then use your screenshot tool).* Suggested set:
1. Dashboard (`app.py`).
2. Searching page: Binary Search mid-run with eliminated range, and the unsorted-array warning.
3. Sorting page: Quick Sort mid-run (colours for compare / swap / sorted).
4. Strassen page: the seven products M1-M7.
5. Dynamic Programming page: LCS table with backtracking path highlighted.
6. Greedy page: Huffman tree and code table.
7. Graph page: Dijkstra with distances on nodes; Kruskal with rejected edges.
8. Performance Analyzer: sorting time chart with theoretical curves.

## 14. Testing and Results
**Framework:** pytest. **Result: 193 tests, all passing** (`pytest -q`).

| Test file | What it checks |
|---|---|
| `test_searching.py` | found / missing, empty, single element, negatives, duplicates, invalid input, comparison counts, step recording |
| `test_sorting.py` | 4 sorts on 10 fixed cases (empty, single, duplicates, negatives, floats, sorted, reverse), 100 random arrays each, input not modified, 1500-element sorted/reverse (no recursion error), invalid input, best/worst-case comparison counts |
| `test_divide_conquer.py` | known 2x2 result, sizes 1-9 and 16 (including non-power-of-two) compared with classical multiplication, identity and zero matrices, floats, leaf size, 7^k vs 8^k multiplication counts, non-square / mismatched / empty / non-numeric input |
| `test_dynamic_programming.py` | textbook cases (15,125 for the CLRS chain), brute-force comparison on random chains and random strings, empty strings, invalid dimensions |
| `test_greedy.py` | textbook cases, brute-force optimality of Activity Selection, fractional knapsack edge cases, Huffman round-trip decoding, prefix-free property, known optimal length (224 bits), invalid input |
| `test_graph_algorithms.py` | BFS/DFS order, disconnected graphs, single vertex, Dijkstra against a Bellman-Ford style check on random graphs, negative-weight rejection, Kruskal against brute force, forests, self-loops, invalid graphs, heap and union-find |
| `test_core.py` | every benchmark suite runs, determinism with the same seed, benchmark validation, input parsers, registry/documentation consistency |
| `test_ui_smoke.py` | every page and every algorithm option renders headlessly without exceptions; every visualizer is stepped through its first, middle and last steps; invalid input shows an error rather than crashing; benchmark button works |

**Bugs found by testing during development:** (1) a hand-computed expected MST weight in a test was wrong (15 instead of 13); the brute-force test confirmed the algorithm was right and the test was corrected. (2) The UI smoke test exposed a crash when drawing the LCS table for strings with repeated letters (duplicate row labels); labels now include the position, e.g. `3: B`.

**Limits of testing:** the automated UI tests verify that pages render and respond; the visual appearance (colours, layout) and the timing of the Play animation should be checked by eye.

## 15. Performance Comparison
All numbers below were **measured by `scripts/run_benchmarks.py`** and are stored in `docs/benchmark_results.md`. They depend on the machine; rerun the script (or the Performance Analyzer page) on your own computer and use your own numbers in your submission.

Machine: Python 3.12.3 on Linux x86_64; 5 repetitions, median time, seed 42.


#### Sorting - scenario: Random

Median time (ms):

|    n |   Heap Sort |   Insertion Sort |   Merge Sort |   Quick Sort |
|-----:|------------:|-----------------:|-------------:|-------------:|
|  100 |      0.2803 |           1.1061 |       0.3081 |       0.2159 |
|  200 |      0.638  |           4.2502 |       0.7051 |       0.4349 |
|  400 |      1.881  |          22.7027 |       1.8296 |       1.6443 |
|  800 |      5.2599 |          98.4775 |       5.5382 |       4.1669 |
| 1600 |      7.3996 |         312.487  |       7.9938 |       6.3529 |

Total operations:

|    n |   Heap Sort |   Insertion Sort |   Merge Sort |   Quick Sort |
|-----:|------------:|-----------------:|-------------:|-------------:|
|  100 |        1632 |             4692 |         1221 |          928 |
|  200 |        3855 |            18774 |         2839 |         2064 |
|  400 |        8849 |            78938 |         6462 |         5153 |
|  800 |       20110 |           308405 |        14501 |        12372 |
| 1600 |       44833 |          1265115 |        32224 |        29341 |


#### Searching - scenario: Target absent (worst case)

Median time (ms):

|      n |   Binary Search |   Linear Search |
|-------:|----------------:|----------------:|
|   1000 |          0.0017 |          0.0501 |
|   5000 |          0.0015 |          0.2544 |
|  20000 |          0.0017 |          1.06   |
| 100000 |          0.002  |          5.1876 |
| 400000 |          0.0023 |         20.7088 |

Total operations:

|      n |   Binary Search |   Linear Search |
|-------:|----------------:|----------------:|
|   1000 |               9 |            1000 |
|   5000 |              12 |            5000 |
|  20000 |              14 |           20000 |
| 100000 |              16 |          100000 |
| 400000 |              18 |          400000 |


#### Divide and Conquer - scenario: Random integer matrices

Median time (ms):

|   n |   Classical |   Strassen |
|----:|------------:|-----------:|
|   2 |      0.0059 |     0.0282 |
|   4 |      0.0084 |     0.1766 |
|   8 |      0.0289 |     1.2106 |
|  16 |      0.1606 |     8.784  |
|  32 |      1.1956 |    66.0095 |
|  64 |     14.0479 |   515.215  |

Total operations:

|   n |   Classical |   Strassen |
|----:|------------:|-----------:|
|   2 |           8 |          7 |
|   4 |          64 |         49 |
|   8 |         512 |        343 |
|  16 |        4096 |       2401 |
|  32 |       32768 |      16807 |
|  64 |      262144 |     117649 |


#### Dynamic Programming - scenario: Random input

Median time (ms):

|   n |     LCS |   Matrix Chain Multiplication |
|----:|--------:|------------------------------:|
|  10 |  0.0894 |                        0.1423 |
|  20 |  0.3665 |                        1.1679 |
|  40 |  1.4008 |                        8.0956 |
|  80 |  5.7775 |                       71.1166 |
| 120 | 13.6606 |                      272.663  |

Total operations:

|   n |   LCS |   Matrix Chain Multiplication |
|----:|------:|------------------------------:|
|  10 |   100 |                           330 |
|  20 |   400 |                          2660 |
|  40 |  1600 |                         21320 |
|  80 |  6400 |                        170640 |
| 120 | 14400 |                        575960 |


#### Greedy Algorithms - scenario: Random input

Median time (ms):

|    n |   Activity Selection |   Fractional Knapsack |   Huffman Coding |
|-----:|---------------------:|----------------------:|-----------------:|
|  100 |               0.1586 |                0.1932 |           0.0582 |
|  500 |               0.9835 |                1.2196 |           0.0977 |
| 1000 |               2.1013 |                3.0996 |           0.127  |
| 2000 |               4.7974 |                6.0651 |           0.2184 |
| 5000 |              15.0612 |               17.772  |           0.4042 |

Total operations:

|    n |   Activity Selection |   Fractional Knapsack |   Huffman Coding |
|-----:|---------------------:|----------------------:|-----------------:|
|  100 |                  100 |                    62 |               24 |
|  500 |                  500 |                   317 |               25 |
| 1000 |                 1000 |                   616 |               25 |
| 2000 |                 2000 |                  1240 |               25 |
| 5000 |                 5000 |                  3134 |               25 |


#### Graph Algorithms - scenario: Random connected graph

Median time (ms):

|   n |    BFS |    DFS |   Dijkstra |   Kruskal |
|----:|-------:|-------:|-----------:|----------:|
|  50 | 0.0207 | 0.0541 |     0.121  |    0.2726 |
| 100 | 0.042  | 0.1035 |     0.293  |    0.6306 |
| 200 | 0.0841 | 0.2016 |     0.7144 |    1.2373 |
| 400 | 0.1867 | 0.4355 |     2.0662 |    2.7433 |
| 800 | 0.417  | 0.924  |     7.8778 |    5.7796 |

Total operations:

|   n |   BFS |   DFS |   Dijkstra |   Kruskal |
|----:|------:|------:|-----------:|----------:|
|  50 |   300 |   300 |        600 |      1017 |
| 100 |   600 |   600 |       1200 |      2315 |
| 200 |  1200 |  1200 |       2400 |      5207 |
| 400 |  2400 |  2400 |       4800 |     11762 |
| 800 |  4800 |  4800 |       9600 |     25999 |


#### Sorting at n = 1000: comparisons by input scenario

|                |   Random |   Already sorted |   Reverse sorted |   Many duplicates |
|:---------------|---------:|-----------------:|-----------------:|------------------:|
| Insertion Sort |   238487 |              999 |           499500 |            216455 |
| Merge Sort     |     8704 |             4932 |             5044 |              8481 |
| Quick Sort     |    10664 |           499500 |           499500 |             54470 |
| Heap Sort      |    16850 |            17583 |            15965 |             15893 |


### Analysis
* **Sorting (random input).** Insertion Sort grows roughly 3-4x when n doubles (quadratic: operations 78,938 -> 308,405 -> 1,265,115 as n goes 400 -> 800 -> 1600, about 4x each time). Merge, Quick and Heap Sort operation counts grow slightly more than 2x per doubling (n log n; e.g. Merge Sort 6,462 -> 14,501). Quick Sort has the fewest operations on random data.
* **Input matters.** At n = 1000, Insertion Sort needs 999 comparisons on sorted input (best case, O(n)) but 499,500 on reverse-sorted input (worst case, n(n-1)/2). Quick Sort with a last-element pivot needs 499,500 comparisons on both sorted and reverse-sorted input, showing its O(n^2) worst case, while Merge and Heap Sort stay near n log n for every scenario.
* **Searching.** The operation count of Linear Search equals n, while Binary Search needs 9, 12, 14, 16 and 18 comparisons (about log2 n + 1). Binary Search's time is nearly flat (a few microseconds, partly timer and call overhead).
* **Strassen versus classical.** Strassen uses fewer multiplications (e.g. 117,649 vs 262,144 at n = 64, exactly 7^k vs 8^k), confirming the theory, **but it is slower in wall-clock time in this implementation** (about 515 ms vs 14 ms at n = 64). The recursion creates many small matrices and performs many additions, and this overhead dominates in Python at these sizes. Theory counts multiplications only; real cost also includes additions, memory allocation and function-call overhead. Practical libraries switch to the classical method below a cut-off size for exactly this reason (the `leaf_size` parameter allows this).
* **Dynamic programming.** LCS operation counts are exactly n^2 (100, 400, 1600, 6400, 14400); Matrix Chain operations grow about 8x per doubling of n (cubic).
* **Greedy.** Activity Selection and Fractional Knapsack time grows slightly faster than linearly (sorting, n log n). Huffman Coding operations stay at 25 (k-1 merges for the 26 letters) regardless of text length; its time grows only because counting characters is O(n).
* **Graphs.** BFS and DFS operation counts are exactly 2E = 6n (each undirected edge examined from both ends) and scale linearly with graph size. Dijkstra and Kruskal take longer in absolute time and their times grow faster than BFS/DFS (e.g. 0.12 -> 7.9 ms for Dijkstra from n = 50 to 800), consistent with the extra log factor from heap operations and sorting. Note that Dijkstra's operation counter counts edge relaxations only, not the heap work, so its count looks linear while its time does not.

### Theoretical versus experimental
Theory describes growth rates and ignores constants; experiments include constants, interpreter overhead, memory effects and timer noise. Operation counts follow theory most cleanly; times follow it for large n but can disagree at small n or when overheads differ between algorithms (Strassen). Both views are needed.

## 16. Conclusion
The project delivers 16 hand-implemented algorithms with step-by-step visualization, complete documentation, a fair benchmarking tool and a 193-test suite. The measurements agree with the theoretical classes where growth rates are concerned and demonstrate an important lesson: asymptotic superiority (Strassen) does not guarantee faster execution at practical input sizes. The separation of logic, visualization and interface keeps the code understandable and testable.

## 17. Future Enhancements
* Add more algorithms (Bellman-Ford, Prim, 0/1 Knapsack, topological sort, string matching).
* Switchable Quick Sort pivot strategies (random, median-of-three) and Merge Sort variants.
* Directed-graph editing and drag-and-drop graph creation.
* Export visualizations as GIF/video; save and share sessions.
* Count additions separately in Strassen; add a cut-off crossover experiment.
* Compare against Python's built-in functions as a reference line in the Performance Analyzer.

## 18. References
1. T. H. Cormen, C. E. Leiserson, R. L. Rivest, C. Stein, *Introduction to Algorithms*, 4th ed., MIT Press, 2022.
2. S. Dasgupta, C. Papadimitriou, U. Vazirani, *Algorithms*, McGraw-Hill, 2008.
3. J. Kleinberg, E. Tardos, *Algorithm Design*, Pearson, 2005.
4. V. Strassen, "Gaussian elimination is not optimal", *Numerische Mathematik* 13, 354-356, 1969.
5. D. A. Huffman, "A method for the construction of minimum-redundancy codes", *Proc. IRE* 40(9), 1098-1101, 1952.
6. E. W. Dijkstra, "A note on two problems in connexion with graphs", *Numerische Mathematik* 1, 269-271, 1959.
7. J. B. Kruskal, "On the shortest spanning subtree of a graph and the traveling salesman problem", *Proc. AMS* 7(1), 48-50, 1956.
8. Streamlit documentation, https://docs.streamlit.io
9. Plotly Python documentation, https://plotly.com/python/
10. NetworkX documentation, https://networkx.org/documentation/stable/
