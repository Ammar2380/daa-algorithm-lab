"""
graph_algorithms.py - BFS, DFS, Dijkstra, Kruskal.

A graph is a dict  {vertex: [(neighbour, weight), ...]}  (adjacency list),
built with build_adjacency(). Step state keys are described in each function.
"""
from collections import deque
from algorithms.data_structures import MinHeap, UnionFind, merge_sort_by
from core.step_tracker import ensure

INF = float("inf")


def validate_graph(vertices, edges):
    if len(set(vertices)) != len(vertices):
        raise ValueError("Vertices must be unique.")
    vset = set(vertices)
    for u, v, w in edges:
        if u not in vset or v not in vset:
            raise ValueError(f"Edge ({u}, {v}) uses an unknown vertex.")
        if isinstance(w, bool) or not isinstance(w, (int, float)):
            raise ValueError(f"Edge ({u}, {v}) has a non-numeric weight.")


def build_adjacency(vertices, edges, directed=False):
    validate_graph(vertices, edges)
    adj = {v: [] for v in vertices}
    for u, v, w in edges:
        adj[u].append((v, w))
        if not directed:
            adj[v].append((u, w))
    return adj


def _check_start(adj, start):
    if start not in adj:
        raise ValueError(f"Start vertex {start!r} is not in the graph.")


def bfs(adj, start, tracker=None):
    """Breadth-first order of vertices reachable from start.
    State keys: visited, frontier (queue), current, tree_edges."""
    t = ensure(tracker)
    _check_start(adj, start)
    visited, order, tree = {start}, [], []
    queue = deque([start])
    if t.recording:
        t.add(f"Start at {start}: mark it visited and put it in the queue.",
              visited=[start], frontier=[start], current=None, tree_edges=[])
    while queue:
        u = queue.popleft()
        order.append(u)
        if t.recording:
            t.add(f"Remove {u} from the queue and explore its neighbours.",
                  visited=list(visited), frontier=list(queue), current=u, tree_edges=list(tree))
        for v, _ in adj[u]:
            t.op()
            if v not in visited:
                visited.add(v)
                queue.append(v)
                tree.append((u, v))
                if t.recording:
                    t.add(f"{v} is new: mark visited and enqueue (edge {u}-{v} joins the BFS tree).",
                          visited=list(visited), frontier=list(queue), current=u, tree_edges=list(tree))
    return order


def dfs(adj, start, tracker=None):
    """Depth-first order from start (explicit stack, same order as the recursive version).
    State keys: visited, frontier (current path), current, tree_edges."""
    t = ensure(tracker)
    _check_start(adj, start)
    visited, order, tree = {start}, [start], []
    stack = [(start, 0)]
    if t.recording:
        t.add(f"Start at {start}: mark it visited.", visited=[start], frontier=[start],
              current=start, tree_edges=[])
    while stack:
        u, i = stack[-1]
        if i < len(adj[u]):
            stack[-1] = (u, i + 1)
            v = adj[u][i][0]
            t.op()
            if v not in visited:
                visited.add(v)
                order.append(v)
                tree.append((u, v))
                stack.append((v, 0))
                if t.recording:
                    t.add(f"Go deeper: {u} -> {v} (new vertex).", visited=list(visited),
                          frontier=[x for x, _ in stack], current=v, tree_edges=list(tree))
        else:
            stack.pop()
            if t.recording and stack:
                t.add(f"{u} has no unvisited neighbours left: backtrack to {stack[-1][0]}.",
                      visited=list(visited), frontier=[x for x, _ in stack],
                      current=stack[-1][0], tree_edges=list(tree))
    return order


def dijkstra(adj, start, tracker=None):
    """Shortest distances from start (non-negative weights only).
    Returns dict(dist, prev). Unreachable vertices keep distance infinity.
    State keys: visited (settled), current, dist, tree_edges, considered (edge)."""
    t = ensure(tracker)
    _check_start(adj, start)
    for u in adj:
        for v, w in adj[u]:
            if w < 0:
                raise ValueError("Dijkstra's algorithm does not allow negative edge weights.")
    dist = {v: INF for v in adj}
    prev = {v: None for v in adj}
    dist[start] = 0
    heap, counter = MinHeap(), 0
    heap.push((0, counter, start))
    settled = []

    def shown():
        return {v: (None if d == INF else d) for v, d in dist.items()}

    def tree():
        return [(prev[v], v) for v in prev if prev[v] is not None]

    if t.recording:
        t.add(f"Start: dist[{start}] = 0, all other distances are infinity.", visited=[],
              current=None, dist=shown(), tree_edges=[], considered=None)
    while len(heap):
        d, _, u = heap.pop()
        if u in settled:
            continue
        settled.append(u)
        if t.recording:
            t.add(f"Pick the unsettled vertex with the smallest distance: {u} ({d}).",
                  visited=list(settled), current=u, dist=shown(), tree_edges=tree(), considered=None)
        for v, w in adj[u]:
            t.op()
            t.compare()
            if d + w < dist[v]:
                dist[v] = d + w
                prev[v] = u
                counter += 1
                heap.push((dist[v], counter, v))
                if t.recording:
                    t.add(f"Relax edge {u}-{v}: {d} + {w} = {d + w} is better, update dist[{v}].",
                          visited=list(settled), current=u, dist=shown(), tree_edges=tree(),
                          considered=(u, v))
    return {"dist": dist, "prev": prev}


def shortest_path(prev, start, target):
    """Rebuild the path start -> target from Dijkstra's `prev` dict ([] if unreachable)."""
    path, node = [], target
    while node is not None:
        path.append(node)
        node = prev[node]
    path = path[::-1]
    return path if path and path[0] == start else []


def kruskal(vertices, edges, tracker=None):
    """Minimum spanning tree (or forest if disconnected).
    Returns dict(mst_edges, total_weight, connected).
    State keys: accepted (edges), rejected (edges), current (edge), sorted_edges."""
    t = ensure(tracker)
    validate_graph(vertices, edges)
    ordered = merge_sort_by(edges, key=lambda e: e[2], tracker=t)
    uf = UnionFind(vertices)
    mst, rejected, total = [], [], 0
    if t.recording:
        t.add("Sort all edges by weight (smallest first).", accepted=[], rejected=[],
              current=None, sorted_edges=list(ordered))
    for edge in ordered:
        u, v, w = edge
        t.op()
        if uf.union(u, v):
            mst.append(edge)
            total += w
            if t.recording:
                t.add(f"Edge {u}-{v} (weight {w}) connects two different components: ACCEPT.",
                      accepted=list(mst), rejected=list(rejected), current=edge, sorted_edges=ordered)
        else:
            rejected.append(edge)
            if t.recording:
                t.add(f"Edge {u}-{v} (weight {w}) would create a cycle: REJECT.",
                      accepted=list(mst), rejected=list(rejected), current=edge, sorted_edges=ordered)
        if len(mst) == len(vertices) - 1:
            break
    return {"mst_edges": mst, "total_weight": total,
            "connected": len(mst) == max(len(vertices) - 1, 0)}
