# Algorithm Reference

Generated from `core/complexity.py`, the same data the app displays.

## Complexity summary

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


## Searching

### Linear Search

1. **Problem definition:** Find the position of a target value in an unordered list.
2. **Input and output:** Input: list A of n values and a target x. Output: index of the first x, or -1.
3. **Step-by-step explanation:**
   - Start at index 0.
   - Compare the current item with the target.
   - If equal, return the index.
   - Otherwise move to the next item.
   - If the end is reached, return -1.
4. **Pseudocode:**

```text
LINEAR-SEARCH(A, x)
  for i = 0 to n-1
    if A[i] == x
      return i
  return -1
```
5. **Python implementation:** `algorithms.searching.linear_search`
6. **Best-case time:** O(1) - target is the first element
7. **Average-case time:** O(n) - about n/2 comparisons
8. **Worst-case time:** O(n) - target is last or absent
9. **Auxiliary space:** O(1)
10. **Real-world applications:** Looking up an item in a small or unsorted list, e.g. finding a name in a short contact list.
11. **Example execution:** A = [5, 3, 8, 1], x = 8 -> compares 5, 3, 8 -> returns index 2 (3 comparisons).

*Notes:* Works on unsorted data. Every element may need to be examined.

### Binary Search

1. **Problem definition:** Find a target in a SORTED list by repeatedly halving the search range.
2. **Input and output:** Input: sorted list A and target x. Output: an index of x, or -1.
3. **Step-by-step explanation:**
   - Set low = 0 and high = n-1.
   - Compute mid = (low + high) // 2.
   - If A[mid] equals x, return mid.
   - If A[mid] < x, search the right half (low = mid + 1).
   - Otherwise search the left half (high = mid - 1).
   - Stop when low > high and return -1.
4. **Pseudocode:**

```text
BINARY-SEARCH(A, x)   // A must be sorted
  low = 0; high = n-1
  while low <= high
    mid = floor((low + high) / 2)
    if A[mid] == x: return mid
    else if A[mid] < x: low = mid + 1
    else: high = mid - 1
  return -1
```
5. **Python implementation:** `algorithms.searching.binary_search`
6. **Best-case time:** O(1) - target is the middle element
7. **Average-case time:** O(log n)
8. **Worst-case time:** O(log n)
9. **Auxiliary space:** O(1) (iterative)
10. **Real-world applications:** Dictionary lookup, searching sorted database indexes, finding a version in a sorted release list.
11. **Example execution:** A = [1, 3, 5, 7, 9], x = 7 -> mid=2 (5<7) -> mid=3 (7) found at index 3 (2 comparisons).

*Notes:* REQUIRES SORTED INPUT. On unsorted data the halving logic can discard the half that contains the target. Recurrence: T(n) = T(n/2) + O(1).


## Sorting

### Insertion Sort

1. **Problem definition:** Sort a list by growing a sorted prefix one element at a time.
2. **Input and output:** Input: list of n numbers. Output: the same numbers in non-decreasing order.
3. **Step-by-step explanation:**
   - Treat the first element as a sorted prefix.
   - Take the next element as the key.
   - Shift larger sorted elements one place to the right.
   - Insert the key into the gap.
   - Repeat until all elements are inserted.
4. **Pseudocode:**

```text
INSERTION-SORT(A)
  for i = 1 to n-1
    key = A[i]; j = i-1
    while j >= 0 and A[j] > key
      A[j+1] = A[j]; j = j-1
    A[j+1] = key
```
5. **Python implementation:** `algorithms.sorting.insertion_sort`
6. **Best-case time:** O(n) - already sorted
7. **Average-case time:** O(n^2)
8. **Worst-case time:** O(n^2) - reverse sorted
9. **Auxiliary space:** O(1)
10. **Real-world applications:** Small arrays, nearly sorted data, and as the final step inside hybrid sorts such as Timsort.
11. **Example execution:** [5, 2, 4] -> insert 2: [2, 5, 4] -> insert 4: [2, 4, 5].

*Notes:* Stable and in-place. Number of shifts equals the number of inversions.

### Merge Sort

1. **Problem definition:** Sort a list by splitting it, sorting both halves, and merging them.
2. **Input and output:** Input: list of n numbers. Output: sorted list.
3. **Step-by-step explanation:**
   - If the range has 0 or 1 element it is sorted.
   - Split the range into two halves.
   - Recursively sort each half.
   - Merge the two sorted halves by repeatedly taking the smaller front element.
4. **Pseudocode:**

```text
MERGE-SORT(A, lo, hi)
  if hi - lo <= 1: return
  mid = (lo + hi) / 2
  MERGE-SORT(A, lo, mid)
  MERGE-SORT(A, mid, hi)
  MERGE(A, lo, mid, hi)
```
5. **Python implementation:** `algorithms.sorting.merge_sort`
6. **Best-case time:** O(n log n)
7. **Average-case time:** O(n log n)
8. **Worst-case time:** O(n log n)
9. **Auxiliary space:** O(n) for the merge buffers
10. **Real-world applications:** Sorting large data sets and linked lists, external sorting of files too big for memory.
11. **Example execution:** [4, 1, 3, 2] -> [4,1] [3,2] -> [1,4] [2,3] -> [1,2,3,4].

*Notes:* Recurrence T(n) = 2T(n/2) + O(n). Stable.

### Quick Sort

1. **Problem definition:** Sort by partitioning around a pivot and sorting each side.
2. **Input and output:** Input: list of n numbers. Output: sorted list.
3. **Step-by-step explanation:**
   - Choose the last element as pivot.
   - Move smaller-or-equal elements before it (Lomuto partition).
   - The pivot is now in its final position.
   - Sort the left and right parts the same way.
4. **Pseudocode:**

```text
QUICKSORT(A, lo, hi)
  if lo < hi
    p = PARTITION(A, lo, hi)
    QUICKSORT(A, lo, p-1)
    QUICKSORT(A, p+1, hi)
PARTITION(A, lo, hi)
  pivot = A[hi]; i = lo-1
  for j = lo to hi-1
    if A[j] <= pivot: i++; swap A[i], A[j]
  swap A[i+1], A[hi]; return i+1
```
5. **Python implementation:** `algorithms.sorting.quick_sort`
6. **Best-case time:** O(n log n) - balanced partitions
7. **Average-case time:** O(n log n)
8. **Worst-case time:** O(n^2) - e.g. already sorted input with last-element pivot
9. **Auxiliary space:** O(log n) average; O(n) worst case in this implementation (explicit stack)
10. **Real-world applications:** General-purpose in-memory sorting; the basis of many library sorts.
11. **Example execution:** [3, 6, 1, 5], pivot 5 -> [3, 1, 5, 6] with 5 fixed at index 2.

*Notes:* Not stable. This version uses an explicit stack so worst-case inputs do not exceed Python's recursion limit.

### Heap Sort

1. **Problem definition:** Sort using a max-heap: repeatedly move the largest element to the end.
2. **Input and output:** Input: list of n numbers. Output: sorted list.
3. **Step-by-step explanation:**
   - Build a max-heap from the array (sift down from the middle to the root).
   - Swap the root (maximum) with the last heap element.
   - Shrink the heap by one.
   - Sift the new root down to restore the heap.
   - Repeat until the heap is empty.
4. **Pseudocode:**

```text
HEAP-SORT(A)
  BUILD-MAX-HEAP(A)
  for end = n-1 down to 1
    swap A[0], A[end]
    SIFT-DOWN(A, 0, end)
```
5. **Python implementation:** `algorithms.sorting.heap_sort`
6. **Best-case time:** O(n log n)
7. **Average-case time:** O(n log n)
8. **Worst-case time:** O(n log n)
9. **Auxiliary space:** O(1)
10. **Real-world applications:** When guaranteed O(n log n) time and O(1) extra space are needed (e.g. embedded systems).
11. **Example execution:** [3, 1, 2] -> heap [3,1,2] -> swap -> [2,1,3] -> sift -> [1,2,3].

*Notes:* Building the heap is O(n); each of the n extractions costs O(log n). Not stable.


## Divide and Conquer

### Strassen's Matrix Multiplication

1. **Problem definition:** Multiply two n x n matrices using 7 recursive multiplications instead of 8.
2. **Input and output:** Input: square matrices A and B of size n. Output: C = A x B (n x n).
3. **Step-by-step explanation:**
   - Pad both matrices with zeros to the next power of two.
   - Split each matrix into four quadrants.
   - Compute seven products M1..M7 from sums/differences of quadrants.
   - Combine: C11 = M1+M4-M5+M7, C12 = M3+M5, C21 = M2+M4, C22 = M1-M2+M3+M6.
   - Recurse until 1x1, then remove the padding.
4. **Pseudocode:**

```text
STRASSEN(A, B)
  if n == 1: return A * B
  split A, B into A11..A22, B11..B22
  M1 = STRASSEN(A11+A22, B11+B22)
  M2 = STRASSEN(A21+A22, B11)
  M3 = STRASSEN(A11, B12-B22)
  M4 = STRASSEN(A22, B21-B11)
  M5 = STRASSEN(A11+A12, B22)
  M6 = STRASSEN(A21-A11, B11+B12)
  M7 = STRASSEN(A12-A22, B21+B22)
  combine C11, C12, C21, C22
```
5. **Python implementation:** `algorithms.divide_conquer.strassen`
6. **Best-case time:** Theta(n^log2(7)) ~ Theta(n^2.81)
7. **Average-case time:** Theta(n^2.81)
8. **Worst-case time:** Theta(n^2.81)
9. **Auxiliary space:** O(n^2) for padding and temporary matrices
10. **Real-world applications:** Large dense matrix products in scientific computing; it is the first algorithm to beat O(n^3).
11. **Example execution:** [[1,2],[3,4]] x [[5,6],[7,8]] = [[19,22],[43,50]] using 7 multiplications.

*Notes:* Recurrence T(n) = 7T(n/2) + Theta(n^2), solved by the Master theorem. Padding to a power of two at most doubles n, which changes only the constant. Because of its overhead, Strassen is often slower than the classical method for small n (see the Performance Analyzer).


## Dynamic Programming

### Matrix Chain Multiplication

1. **Problem definition:** Find the parenthesization of a chain of matrices that needs the fewest scalar multiplications.
2. **Input and output:** Input: dimensions p0..pn (matrix Ai is p(i-1) x p(i)). Output: minimum cost and parenthesization.
3. **Step-by-step explanation:**
   - m[i][i] = 0 for single matrices.
   - For chain length L = 2..n, for every start i, set j = i+L-1.
   - Try every split k between i and j-1.
   - Cost = m[i][k] + m[k+1][j] + p(i-1)*p(k)*p(j).
   - Keep the minimum in m[i][j] and the best k in s[i][j].
   - Rebuild the order from s.
4. **Pseudocode:**

```text
MATRIX-CHAIN-ORDER(p)
  for i = 1 to n: m[i][i] = 0
  for L = 2 to n
    for i = 1 to n-L+1
      j = i+L-1; m[i][j] = infinity
      for k = i to j-1
        q = m[i][k] + m[k+1][j] + p[i-1]*p[k]*p[j]
        if q < m[i][j]: m[i][j] = q; s[i][j] = k
```
5. **Python implementation:** `algorithms.dynamic_programming.matrix_chain_order`
6. **Best-case time:** Theta(n^3)
7. **Average-case time:** Theta(n^3)
8. **Worst-case time:** Theta(n^3)
9. **Auxiliary space:** Theta(n^2) for the m and s tables
10. **Real-world applications:** Query optimization in databases, compilers choosing evaluation order, graphics pipelines.
11. **Example execution:** p = [10, 20, 30]: one split, cost 10*20*30 = 6000.

*Notes:* Recurrence: m[i][j] = min over i<=k<j of (m[i][k] + m[k+1][j] + p(i-1)p(k)p(j)). There are O(n^2) subproblems and O(n) work each. n is the number of matrices.

### Longest Common Subsequence (LCS)

1. **Problem definition:** Find the longest sequence of characters that appears in both strings in the same order (not necessarily contiguous).
2. **Input and output:** Input: strings X (length m) and Y (length n). Output: length and one LCS.
3. **Step-by-step explanation:**
   - Create a table L of size (m+1) x (n+1) filled with 0.
   - If X[i] == Y[j], L[i][j] = L[i-1][j-1] + 1.
   - Otherwise L[i][j] = max(L[i-1][j], L[i][j-1]).
   - L[m][n] is the LCS length.
   - Backtrack from (m, n) to recover the subsequence.
4. **Pseudocode:**

```text
LCS(X, Y)
  for i = 1 to m
    for j = 1 to n
      if X[i] == Y[j]: L[i][j] = L[i-1][j-1] + 1
      else: L[i][j] = max(L[i-1][j], L[i][j-1])
  return L[m][n]
```
5. **Python implementation:** `algorithms.dynamic_programming.lcs`
6. **Best-case time:** Theta(mn)
7. **Average-case time:** Theta(mn)
8. **Worst-case time:** Theta(mn)
9. **Auxiliary space:** Theta(mn) (needed to backtrack)
10. **Real-world applications:** File difference tools (diff), DNA sequence comparison, plagiarism detection.
11. **Example execution:** X = ABCBDAB, Y = BDCABA -> LCS length 4 (e.g. BCBA).

*Notes:* Every cell is computed once, so time is Theta(mn) in all cases. Length alone can be computed in O(min(m,n)) space; this project keeps the full table to show it and to rebuild the subsequence.


## Greedy Algorithms

### Activity Selection

1. **Problem definition:** Choose the maximum number of non-overlapping activities.
2. **Input and output:** Input: list of (start, finish). Output: indices of a largest compatible set.
3. **Step-by-step explanation:**
   - Sort activities by finish time.
   - Select the first activity.
   - For each next activity, select it if its start >= finish of the last selected.
   - Skip the others.
4. **Pseudocode:**

```text
ACTIVITY-SELECTION(a)
  sort a by finish time
  S = {a[0]}; last = a[0].finish
  for each activity i in order
    if a[i].start >= last: S = S + {a[i]}; last = a[i].finish
  return S
```
5. **Python implementation:** `algorithms.greedy.activity_selection`
6. **Best-case time:** O(n log n)
7. **Average-case time:** O(n log n)
8. **Worst-case time:** O(n log n)
9. **Auxiliary space:** O(n)
10. **Real-world applications:** Scheduling rooms, machines or CPU time slots.
11. **Example execution:** (1,4) (3,5) (5,7) -> selects (1,4) and (5,7).

*Notes:* Sorting dominates (O(n log n)); the scan is O(n). Greedy choice: earliest finish time leaves the most room - proven optimal by an exchange argument.

### Fractional Knapsack

1. **Problem definition:** Fill a knapsack of limited capacity to maximise value when items can be split.
2. **Input and output:** Input: items (value, weight) and capacity W. Output: maximum value and the fraction of each item taken.
3. **Step-by-step explanation:**
   - Compute value/weight for every item.
   - Sort by ratio, highest first.
   - Take whole items while they fit.
   - Take a fraction of the next item to fill the remaining capacity.
4. **Pseudocode:**

```text
FRACTIONAL-KNAPSACK(items, W)
  sort items by value/weight descending
  for each item
    if weight <= W: take all; W = W - weight
    else: take fraction W/weight; break
```
5. **Python implementation:** `algorithms.greedy.fractional_knapsack`
6. **Best-case time:** O(n log n)
7. **Average-case time:** O(n log n)
8. **Worst-case time:** O(n log n)
9. **Auxiliary space:** O(n)
10. **Real-world applications:** Resource allocation, loading cargo of divisible goods (grain, liquids), portfolio budgeting.
11. **Example execution:** (60,10) (100,20) (120,30), W = 50 -> value 240.

*Notes:* Greedy is optimal here because items are divisible. It is NOT optimal for the 0/1 knapsack.

### Huffman Coding

1. **Problem definition:** Build an optimal prefix-free binary code that minimises the encoded length of a text.
2. **Input and output:** Input: a text. Output: code for each character and the encoded bit string.
3. **Step-by-step explanation:**
   - Count the frequency of every character.
   - Put one leaf per character in a min-heap.
   - Repeatedly remove the two smallest nodes and merge them into a parent with the summed frequency.
   - Continue until one node (the root) remains.
   - Left edge = 0, right edge = 1; the path to a leaf is its code.
4. **Pseudocode:**

```text
HUFFMAN(C)
  Q = min-heap of leaves C
  while |Q| > 1
    x = EXTRACT-MIN(Q); y = EXTRACT-MIN(Q)
    z = new node(freq = x.freq + y.freq, left = x, right = y)
    INSERT(Q, z)
  return EXTRACT-MIN(Q)
```
5. **Python implementation:** `algorithms.greedy.huffman_coding`
6. **Best-case time:** O(n) - only one distinct character
7. **Average-case time:** O(n + k log k)
8. **Worst-case time:** O(n + k log k), k = number of distinct characters
9. **Auxiliary space:** O(k)
10. **Real-world applications:** File compression (ZIP/DEFLATE, JPEG, MP3 use Huffman stages).
11. **Example execution:** 'abracadabra' -> 'a' gets the shortest code because it is the most frequent.

*Notes:* Counting frequencies is O(n); the heap work is O(k log k) because there are k-1 merges, each O(log k). The codes are prefix-free so decoding is unambiguous.


## Graph Algorithms

### Breadth-First Search (BFS)

1. **Problem definition:** Visit all vertices reachable from a start vertex, level by level.
2. **Input and output:** Input: graph and start vertex. Output: vertices in visiting order.
3. **Step-by-step explanation:**
   - Mark the start visited and enqueue it.
   - Dequeue a vertex.
   - Enqueue all its unvisited neighbours and mark them visited.
   - Repeat until the queue is empty.
4. **Pseudocode:**

```text
BFS(G, s)
  mark s visited; Q = [s]
  while Q not empty
    u = DEQUEUE(Q)
    for each neighbour v of u
      if v not visited: mark v; ENQUEUE(Q, v)
```
5. **Python implementation:** `algorithms.graph_algorithms.bfs`
6. **Best-case time:** O(V + E)
7. **Average-case time:** O(V + E)
8. **Worst-case time:** O(V + E)
9. **Auxiliary space:** O(V)
10. **Real-world applications:** Shortest path in unweighted graphs, social-network 'degrees of separation', web crawlers.
11. **Example execution:** A-B, A-C, B-D from A -> A, B, C, D.

*Notes:* With an adjacency list every vertex and every edge is processed a constant number of times. Only the connected component of the start vertex is visited.

### Depth-First Search (DFS)

1. **Problem definition:** Visit all vertices reachable from a start vertex by going as deep as possible before backtracking.
2. **Input and output:** Input: graph and start vertex. Output: vertices in visiting order.
3. **Step-by-step explanation:**
   - Mark the start visited.
   - Move to the first unvisited neighbour and repeat.
   - When no unvisited neighbour exists, backtrack.
   - Stop when backtracking returns to the start with nothing left.
4. **Pseudocode:**

```text
DFS(G, u)
  mark u visited
  for each neighbour v of u
    if v not visited: DFS(G, v)
```
5. **Python implementation:** `algorithms.graph_algorithms.dfs`
6. **Best-case time:** O(V + E)
7. **Average-case time:** O(V + E)
8. **Worst-case time:** O(V + E)
9. **Auxiliary space:** O(V) for the visited set and stack
10. **Real-world applications:** Cycle detection, topological sorting, maze solving, finding connected components.
11. **Example execution:** A-B, A-C, B-D from A -> A, B, D, C.

*Notes:* This project uses an explicit stack (same order as recursion) so deep graphs do not hit Python's recursion limit.

### Dijkstra's Shortest Path

1. **Problem definition:** Find the shortest distance from one source vertex to every other vertex in a graph with non-negative weights.
2. **Input and output:** Input: weighted graph and source. Output: shortest distance to each vertex and the path tree.
3. **Step-by-step explanation:**
   - Set dist[source] = 0 and all others to infinity.
   - Repeatedly pick the unsettled vertex u with the smallest distance.
   - For each edge (u, v, w): if dist[u] + w < dist[v], update dist[v] (relaxation).
   - Mark u settled and repeat.
4. **Pseudocode:**

```text
DIJKSTRA(G, s)
  dist[v] = infinity for all v; dist[s] = 0
  Q = min-heap with (0, s)
  while Q not empty
    u = EXTRACT-MIN(Q)
    for each edge (u, v, w)
      if dist[u] + w < dist[v]: dist[v] = dist[u] + w; INSERT(Q, v)
```
5. **Python implementation:** `algorithms.graph_algorithms.dijkstra`
6. **Best-case time:** O((V + E) log V)
7. **Average-case time:** O((V + E) log V)
8. **Worst-case time:** O((V + E) log V)
9. **Auxiliary space:** O(V + E)
10. **Real-world applications:** GPS navigation, network routing protocols (OSPF), flight planning.
11. **Example execution:** A-B 4, A-C 2, C-B 1 from A -> dist B = 3 (via C).

*Notes:* Binary-heap version with lazy deletion. Fails with negative edge weights, so the code rejects them. Unreachable vertices keep distance infinity.

### Kruskal's Minimum Spanning Tree

1. **Problem definition:** Connect all vertices with edges of minimum total weight and no cycles.
2. **Input and output:** Input: weighted undirected graph. Output: MST edges and total weight (a forest if disconnected).
3. **Step-by-step explanation:**
   - Sort all edges by weight.
   - Take the lightest unused edge.
   - Add it if its endpoints are in different components (checked with Union-Find).
   - Otherwise skip it (it would form a cycle).
   - Stop after V-1 edges.
4. **Pseudocode:**

```text
KRUSKAL(G)
  A = {}; make-set(v) for each v
  sort edges by weight
  for each edge (u, v) in order
    if FIND(u) != FIND(v): A = A + {(u, v)}; UNION(u, v)
  return A
```
5. **Python implementation:** `algorithms.graph_algorithms.kruskal`
6. **Best-case time:** O(E log E)
7. **Average-case time:** O(E log E)
8. **Worst-case time:** O(E log E) = O(E log V)
9. **Auxiliary space:** O(V + E)
10. **Real-world applications:** Designing cable, pipeline or road networks at minimum cost; clustering.
11. **Example execution:** Triangle A-B 1, B-C 2, A-C 3 -> picks A-B and B-C, total 3.

*Notes:* Sorting costs O(E log E); the Union-Find operations are almost O(1) each. The code may stop early once V-1 edges are chosen.
