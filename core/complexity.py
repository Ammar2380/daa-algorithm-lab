"""
complexity.py - Documentation data for every algorithm (single source of truth).

The Algorithm Explorer panels and docs/algorithm_reference.md are both generated from
ALGORITHM_INFO, so the text shown in the app and in the report always agree.
Also contains the theoretical growth functions used to draw reference curves.
"""
import math

# ------------------------------------------------------------ growth functions
def f_n(n): return n
def f_n2(n): return n * n
def f_n3(n): return n ** 3
def f_nlogn(n): return n * math.log2(n) if n > 1 else 1
def f_logn(n): return math.log2(n) if n > 1 else 1
def f_strassen(n): return n ** math.log2(7)


def _info(name, category, function, problem, io, application, how, pseudo,
          best, average, worst, space, notes, example):
    return {"name": name, "category": category, "function": function, "problem": problem,
            "input_output": io, "application": application, "how_it_works": how,
            "pseudocode": pseudo, "best": best, "average": average, "worst": worst,
            "space": space, "notes": notes, "example": example}


ALGORITHM_INFO = {}


def _add(**kw):
    info = _info(**kw)
    ALGORITHM_INFO[info["name"]] = info


_add(name="Linear Search", category="Searching", function="algorithms.searching.linear_search",
     problem="Find the position of a target value in an unordered list.",
     io="Input: list A of n values and a target x. Output: index of the first x, or -1.",
     application="Looking up an item in a small or unsorted list, e.g. finding a name in a short contact list.",
     how=["Start at index 0.", "Compare the current item with the target.",
          "If equal, return the index.", "Otherwise move to the next item.",
          "If the end is reached, return -1."],
     pseudo="LINEAR-SEARCH(A, x)\n  for i = 0 to n-1\n    if A[i] == x\n      return i\n  return -1",
     best="O(1) - target is the first element", average="O(n) - about n/2 comparisons",
     worst="O(n) - target is last or absent", space="O(1)",
     notes="Works on unsorted data. Every element may need to be examined.",
     example="A = [5, 3, 8, 1], x = 8 -> compares 5, 3, 8 -> returns index 2 (3 comparisons).")

_add(name="Binary Search", category="Searching", function="algorithms.searching.binary_search",
     problem="Find a target in a SORTED list by repeatedly halving the search range.",
     io="Input: sorted list A and target x. Output: an index of x, or -1.",
     application="Dictionary lookup, searching sorted database indexes, finding a version in a sorted release list.",
     how=["Set low = 0 and high = n-1.", "Compute mid = (low + high) // 2.",
          "If A[mid] equals x, return mid.", "If A[mid] < x, search the right half (low = mid + 1).",
          "Otherwise search the left half (high = mid - 1).", "Stop when low > high and return -1."],
     pseudo="BINARY-SEARCH(A, x)   // A must be sorted\n  low = 0; high = n-1\n  while low <= high\n    mid = floor((low + high) / 2)\n    if A[mid] == x: return mid\n    else if A[mid] < x: low = mid + 1\n    else: high = mid - 1\n  return -1",
     best="O(1) - target is the middle element", average="O(log n)", worst="O(log n)",
     space="O(1) (iterative)",
     notes="REQUIRES SORTED INPUT. On unsorted data the halving logic can discard the half that contains the target. Recurrence: T(n) = T(n/2) + O(1).",
     example="A = [1, 3, 5, 7, 9], x = 7 -> mid=2 (5<7) -> mid=3 (7) found at index 3 (2 comparisons).")

_add(name="Insertion Sort", category="Sorting", function="algorithms.sorting.insertion_sort",
     problem="Sort a list by growing a sorted prefix one element at a time.",
     io="Input: list of n numbers. Output: the same numbers in non-decreasing order.",
     application="Small arrays, nearly sorted data, and as the final step inside hybrid sorts such as Timsort.",
     how=["Treat the first element as a sorted prefix.", "Take the next element as the key.",
          "Shift larger sorted elements one place to the right.", "Insert the key into the gap.",
          "Repeat until all elements are inserted."],
     pseudo="INSERTION-SORT(A)\n  for i = 1 to n-1\n    key = A[i]; j = i-1\n    while j >= 0 and A[j] > key\n      A[j+1] = A[j]; j = j-1\n    A[j+1] = key",
     best="O(n) - already sorted", average="O(n^2)", worst="O(n^2) - reverse sorted",
     space="O(1)", notes="Stable and in-place. Number of shifts equals the number of inversions.",
     example="[5, 2, 4] -> insert 2: [2, 5, 4] -> insert 4: [2, 4, 5].")

_add(name="Merge Sort", category="Sorting", function="algorithms.sorting.merge_sort",
     problem="Sort a list by splitting it, sorting both halves, and merging them.",
     io="Input: list of n numbers. Output: sorted list.",
     application="Sorting large data sets and linked lists, external sorting of files too big for memory.",
     how=["If the range has 0 or 1 element it is sorted.", "Split the range into two halves.",
          "Recursively sort each half.", "Merge the two sorted halves by repeatedly taking the smaller front element."],
     pseudo="MERGE-SORT(A, lo, hi)\n  if hi - lo <= 1: return\n  mid = (lo + hi) / 2\n  MERGE-SORT(A, lo, mid)\n  MERGE-SORT(A, mid, hi)\n  MERGE(A, lo, mid, hi)",
     best="O(n log n)", average="O(n log n)", worst="O(n log n)", space="O(n) for the merge buffers",
     notes="Recurrence T(n) = 2T(n/2) + O(n). Stable.",
     example="[4, 1, 3, 2] -> [4,1] [3,2] -> [1,4] [2,3] -> [1,2,3,4].")

_add(name="Quick Sort", category="Sorting", function="algorithms.sorting.quick_sort",
     problem="Sort by partitioning around a pivot and sorting each side.",
     io="Input: list of n numbers. Output: sorted list.",
     application="General-purpose in-memory sorting; the basis of many library sorts.",
     how=["Choose the last element as pivot.", "Move smaller-or-equal elements before it (Lomuto partition).",
          "The pivot is now in its final position.", "Sort the left and right parts the same way."],
     pseudo="QUICKSORT(A, lo, hi)\n  if lo < hi\n    p = PARTITION(A, lo, hi)\n    QUICKSORT(A, lo, p-1)\n    QUICKSORT(A, p+1, hi)\nPARTITION(A, lo, hi)\n  pivot = A[hi]; i = lo-1\n  for j = lo to hi-1\n    if A[j] <= pivot: i++; swap A[i], A[j]\n  swap A[i+1], A[hi]; return i+1",
     best="O(n log n) - balanced partitions", average="O(n log n)",
     worst="O(n^2) - e.g. already sorted input with last-element pivot",
     space="O(log n) average; O(n) worst case in this implementation (explicit stack)",
     notes="Not stable. This version uses an explicit stack so worst-case inputs do not exceed Python's recursion limit.",
     example="[3, 6, 1, 5], pivot 5 -> [3, 1, 5, 6] with 5 fixed at index 2.")

_add(name="Heap Sort", category="Sorting", function="algorithms.sorting.heap_sort",
     problem="Sort using a max-heap: repeatedly move the largest element to the end.",
     io="Input: list of n numbers. Output: sorted list.",
     application="When guaranteed O(n log n) time and O(1) extra space are needed (e.g. embedded systems).",
     how=["Build a max-heap from the array (sift down from the middle to the root).",
          "Swap the root (maximum) with the last heap element.", "Shrink the heap by one.",
          "Sift the new root down to restore the heap.", "Repeat until the heap is empty."],
     pseudo="HEAP-SORT(A)\n  BUILD-MAX-HEAP(A)\n  for end = n-1 down to 1\n    swap A[0], A[end]\n    SIFT-DOWN(A, 0, end)",
     best="O(n log n)", average="O(n log n)", worst="O(n log n)", space="O(1)",
     notes="Building the heap is O(n); each of the n extractions costs O(log n). Not stable.",
     example="[3, 1, 2] -> heap [3,1,2] -> swap -> [2,1,3] -> sift -> [1,2,3].")

_add(name="Strassen's Matrix Multiplication", category="Divide and Conquer",
     function="algorithms.divide_conquer.strassen",
     problem="Multiply two n x n matrices using 7 recursive multiplications instead of 8.",
     io="Input: square matrices A and B of size n. Output: C = A x B (n x n).",
     application="Large dense matrix products in scientific computing; it is the first algorithm to beat O(n^3).",
     how=["Pad both matrices with zeros to the next power of two.", "Split each matrix into four quadrants.",
          "Compute seven products M1..M7 from sums/differences of quadrants.",
          "Combine: C11 = M1+M4-M5+M7, C12 = M3+M5, C21 = M2+M4, C22 = M1-M2+M3+M6.",
          "Recurse until 1x1, then remove the padding."],
     pseudo="STRASSEN(A, B)\n  if n == 1: return A * B\n  split A, B into A11..A22, B11..B22\n  M1 = STRASSEN(A11+A22, B11+B22)\n  M2 = STRASSEN(A21+A22, B11)\n  M3 = STRASSEN(A11, B12-B22)\n  M4 = STRASSEN(A22, B21-B11)\n  M5 = STRASSEN(A11+A12, B22)\n  M6 = STRASSEN(A21-A11, B11+B12)\n  M7 = STRASSEN(A12-A22, B21+B22)\n  combine C11, C12, C21, C22",
     best="Theta(n^log2(7)) ~ Theta(n^2.81)", average="Theta(n^2.81)", worst="Theta(n^2.81)",
     space="O(n^2) for padding and temporary matrices",
     notes="Recurrence T(n) = 7T(n/2) + Theta(n^2), solved by the Master theorem. Padding to a power of two at most doubles n, which changes only the constant. Because of its overhead, Strassen is often slower than the classical method for small n (see the Performance Analyzer).",
     example="[[1,2],[3,4]] x [[5,6],[7,8]] = [[19,22],[43,50]] using 7 multiplications.")

_add(name="Matrix Chain Multiplication", category="Dynamic Programming",
     function="algorithms.dynamic_programming.matrix_chain_order",
     problem="Find the parenthesization of a chain of matrices that needs the fewest scalar multiplications.",
     io="Input: dimensions p0..pn (matrix Ai is p(i-1) x p(i)). Output: minimum cost and parenthesization.",
     application="Query optimization in databases, compilers choosing evaluation order, graphics pipelines.",
     how=["m[i][i] = 0 for single matrices.", "For chain length L = 2..n, for every start i, set j = i+L-1.",
          "Try every split k between i and j-1.", "Cost = m[i][k] + m[k+1][j] + p(i-1)*p(k)*p(j).",
          "Keep the minimum in m[i][j] and the best k in s[i][j].", "Rebuild the order from s."],
     pseudo="MATRIX-CHAIN-ORDER(p)\n  for i = 1 to n: m[i][i] = 0\n  for L = 2 to n\n    for i = 1 to n-L+1\n      j = i+L-1; m[i][j] = infinity\n      for k = i to j-1\n        q = m[i][k] + m[k+1][j] + p[i-1]*p[k]*p[j]\n        if q < m[i][j]: m[i][j] = q; s[i][j] = k",
     best="Theta(n^3)", average="Theta(n^3)", worst="Theta(n^3)", space="Theta(n^2) for the m and s tables",
     notes="Recurrence: m[i][j] = min over i<=k<j of (m[i][k] + m[k+1][j] + p(i-1)p(k)p(j)). There are O(n^2) subproblems and O(n) work each. n is the number of matrices.",
     example="p = [10, 20, 30]: one split, cost 10*20*30 = 6000.")

_add(name="Longest Common Subsequence (LCS)", category="Dynamic Programming",
     function="algorithms.dynamic_programming.lcs",
     problem="Find the longest sequence of characters that appears in both strings in the same order (not necessarily contiguous).",
     io="Input: strings X (length m) and Y (length n). Output: length and one LCS.",
     application="File difference tools (diff), DNA sequence comparison, plagiarism detection.",
     how=["Create a table L of size (m+1) x (n+1) filled with 0.",
          "If X[i] == Y[j], L[i][j] = L[i-1][j-1] + 1.", "Otherwise L[i][j] = max(L[i-1][j], L[i][j-1]).",
          "L[m][n] is the LCS length.", "Backtrack from (m, n) to recover the subsequence."],
     pseudo="LCS(X, Y)\n  for i = 1 to m\n    for j = 1 to n\n      if X[i] == Y[j]: L[i][j] = L[i-1][j-1] + 1\n      else: L[i][j] = max(L[i-1][j], L[i][j-1])\n  return L[m][n]",
     best="Theta(mn)", average="Theta(mn)", worst="Theta(mn)", space="Theta(mn) (needed to backtrack)",
     notes="Every cell is computed once, so time is Theta(mn) in all cases. Length alone can be computed in O(min(m,n)) space; this project keeps the full table to show it and to rebuild the subsequence.",
     example="X = ABCBDAB, Y = BDCABA -> LCS length 4 (e.g. BCBA).")

_add(name="Activity Selection", category="Greedy Algorithms", function="algorithms.greedy.activity_selection",
     problem="Choose the maximum number of non-overlapping activities.",
     io="Input: list of (start, finish). Output: indices of a largest compatible set.",
     application="Scheduling rooms, machines or CPU time slots.",
     how=["Sort activities by finish time.", "Select the first activity.",
          "For each next activity, select it if its start >= finish of the last selected.", "Skip the others."],
     pseudo="ACTIVITY-SELECTION(a)\n  sort a by finish time\n  S = {a[0]}; last = a[0].finish\n  for each activity i in order\n    if a[i].start >= last: S = S + {a[i]}; last = a[i].finish\n  return S",
     best="O(n log n)", average="O(n log n)", worst="O(n log n)", space="O(n)",
     notes="Sorting dominates (O(n log n)); the scan is O(n). Greedy choice: earliest finish time leaves the most room - proven optimal by an exchange argument.",
     example="(1,4) (3,5) (5,7) -> selects (1,4) and (5,7).")

_add(name="Fractional Knapsack", category="Greedy Algorithms", function="algorithms.greedy.fractional_knapsack",
     problem="Fill a knapsack of limited capacity to maximise value when items can be split.",
     io="Input: items (value, weight) and capacity W. Output: maximum value and the fraction of each item taken.",
     application="Resource allocation, loading cargo of divisible goods (grain, liquids), portfolio budgeting.",
     how=["Compute value/weight for every item.", "Sort by ratio, highest first.",
          "Take whole items while they fit.", "Take a fraction of the next item to fill the remaining capacity."],
     pseudo="FRACTIONAL-KNAPSACK(items, W)\n  sort items by value/weight descending\n  for each item\n    if weight <= W: take all; W = W - weight\n    else: take fraction W/weight; break",
     best="O(n log n)", average="O(n log n)", worst="O(n log n)", space="O(n)",
     notes="Greedy is optimal here because items are divisible. It is NOT optimal for the 0/1 knapsack.",
     example="(60,10) (100,20) (120,30), W = 50 -> value 240.")

_add(name="Huffman Coding", category="Greedy Algorithms", function="algorithms.greedy.huffman_coding",
     problem="Build an optimal prefix-free binary code that minimises the encoded length of a text.",
     io="Input: a text. Output: code for each character and the encoded bit string.",
     application="File compression (ZIP/DEFLATE, JPEG, MP3 use Huffman stages).",
     how=["Count the frequency of every character.", "Put one leaf per character in a min-heap.",
          "Repeatedly remove the two smallest nodes and merge them into a parent with the summed frequency.",
          "Continue until one node (the root) remains.", "Left edge = 0, right edge = 1; the path to a leaf is its code."],
     pseudo="HUFFMAN(C)\n  Q = min-heap of leaves C\n  while |Q| > 1\n    x = EXTRACT-MIN(Q); y = EXTRACT-MIN(Q)\n    z = new node(freq = x.freq + y.freq, left = x, right = y)\n    INSERT(Q, z)\n  return EXTRACT-MIN(Q)",
     best="O(n) - only one distinct character", average="O(n + k log k)", worst="O(n + k log k), k = number of distinct characters",
     space="O(k)",
     notes="Counting frequencies is O(n); the heap work is O(k log k) because there are k-1 merges, each O(log k). The codes are prefix-free so decoding is unambiguous.",
     example="'abracadabra' -> 'a' gets the shortest code because it is the most frequent.")

_add(name="Breadth-First Search (BFS)", category="Graph Algorithms", function="algorithms.graph_algorithms.bfs",
     problem="Visit all vertices reachable from a start vertex, level by level.",
     io="Input: graph and start vertex. Output: vertices in visiting order.",
     application="Shortest path in unweighted graphs, social-network 'degrees of separation', web crawlers.",
     how=["Mark the start visited and enqueue it.", "Dequeue a vertex.",
          "Enqueue all its unvisited neighbours and mark them visited.", "Repeat until the queue is empty."],
     pseudo="BFS(G, s)\n  mark s visited; Q = [s]\n  while Q not empty\n    u = DEQUEUE(Q)\n    for each neighbour v of u\n      if v not visited: mark v; ENQUEUE(Q, v)",
     best="O(V + E)", average="O(V + E)", worst="O(V + E)", space="O(V)",
     notes="With an adjacency list every vertex and every edge is processed a constant number of times. Only the connected component of the start vertex is visited.",
     example="A-B, A-C, B-D from A -> A, B, C, D.")

_add(name="Depth-First Search (DFS)", category="Graph Algorithms", function="algorithms.graph_algorithms.dfs",
     problem="Visit all vertices reachable from a start vertex by going as deep as possible before backtracking.",
     io="Input: graph and start vertex. Output: vertices in visiting order.",
     application="Cycle detection, topological sorting, maze solving, finding connected components.",
     how=["Mark the start visited.", "Move to the first unvisited neighbour and repeat.",
          "When no unvisited neighbour exists, backtrack.", "Stop when backtracking returns to the start with nothing left."],
     pseudo="DFS(G, u)\n  mark u visited\n  for each neighbour v of u\n    if v not visited: DFS(G, v)",
     best="O(V + E)", average="O(V + E)", worst="O(V + E)", space="O(V) for the visited set and stack",
     notes="This project uses an explicit stack (same order as recursion) so deep graphs do not hit Python's recursion limit.",
     example="A-B, A-C, B-D from A -> A, B, D, C.")

_add(name="Dijkstra's Shortest Path", category="Graph Algorithms", function="algorithms.graph_algorithms.dijkstra",
     problem="Find the shortest distance from one source vertex to every other vertex in a graph with non-negative weights.",
     io="Input: weighted graph and source. Output: shortest distance to each vertex and the path tree.",
     application="GPS navigation, network routing protocols (OSPF), flight planning.",
     how=["Set dist[source] = 0 and all others to infinity.", "Repeatedly pick the unsettled vertex u with the smallest distance.",
          "For each edge (u, v, w): if dist[u] + w < dist[v], update dist[v] (relaxation).", "Mark u settled and repeat."],
     pseudo="DIJKSTRA(G, s)\n  dist[v] = infinity for all v; dist[s] = 0\n  Q = min-heap with (0, s)\n  while Q not empty\n    u = EXTRACT-MIN(Q)\n    for each edge (u, v, w)\n      if dist[u] + w < dist[v]: dist[v] = dist[u] + w; INSERT(Q, v)",
     best="O((V + E) log V)", average="O((V + E) log V)", worst="O((V + E) log V)", space="O(V + E)",
     notes="Binary-heap version with lazy deletion. Fails with negative edge weights, so the code rejects them. Unreachable vertices keep distance infinity.",
     example="A-B 4, A-C 2, C-B 1 from A -> dist B = 3 (via C).")

_add(name="Kruskal's Minimum Spanning Tree", category="Graph Algorithms", function="algorithms.graph_algorithms.kruskal",
     problem="Connect all vertices with edges of minimum total weight and no cycles.",
     io="Input: weighted undirected graph. Output: MST edges and total weight (a forest if disconnected).",
     application="Designing cable, pipeline or road networks at minimum cost; clustering.",
     how=["Sort all edges by weight.", "Take the lightest unused edge.",
          "Add it if its endpoints are in different components (checked with Union-Find).", "Otherwise skip it (it would form a cycle).",
          "Stop after V-1 edges."],
     pseudo="KRUSKAL(G)\n  A = {}; make-set(v) for each v\n  sort edges by weight\n  for each edge (u, v) in order\n    if FIND(u) != FIND(v): A = A + {(u, v)}; UNION(u, v)\n  return A",
     best="O(E log E)", average="O(E log E)", worst="O(E log E) = O(E log V)", space="O(V + E)",
     notes="Sorting costs O(E log E); the Union-Find operations are almost O(1) each. The code may stop early once V-1 edges are chosen.",
     example="Triangle A-B 1, B-C 2, A-C 3 -> picks A-B and B-C, total 3.")

CATEGORY_ORDER = ["Searching", "Sorting", "Divide and Conquer", "Dynamic Programming",
                  "Greedy Algorithms", "Graph Algorithms"]
