import itertools
import random
import pytest
from algorithms.graph_algorithms import (build_adjacency, bfs, dfs, dijkstra, kruskal,
                                         shortest_path, INF)
from algorithms.data_structures import MinHeap, UnionFind, merge_sort_by

V = ["A", "B", "C", "D", "E", "F"]
E = [("A", "B", 4), ("A", "C", 2), ("B", "C", 1), ("B", "D", 5), ("C", "D", 8),
     ("C", "E", 10), ("D", "E", 2), ("D", "F", 6), ("E", "F", 3)]


def test_bfs_and_dfs_order():
    adj = build_adjacency(V, E)
    assert bfs(adj, "A") == ["A", "B", "C", "D", "E", "F"]
    assert dfs(adj, "A") == ["A", "B", "C", "D", "E", "F"]


def test_dfs_goes_deep_first():
    adj = build_adjacency(["1", "2", "3", "4"], [("1", "2", 1), ("1", "3", 1), ("2", "4", 1)])
    assert dfs(adj, "1") == ["1", "2", "4", "3"]
    assert bfs(adj, "1") == ["1", "2", "3", "4"]


def test_traversal_edge_cases_disconnected():
    adj = build_adjacency(["A", "B", "C"], [("A", "B", 1)])
    assert bfs(adj, "A") == ["A", "B"] and dfs(adj, "C") == ["C"]
    assert bfs(build_adjacency(["X"], []), "X") == ["X"]


def test_bad_start_vertex():
    adj = build_adjacency(V, E)
    for f in (bfs, dfs, dijkstra):
        with pytest.raises(ValueError):
            f(adj, "Z")


def test_dijkstra_known():
    adj = build_adjacency(V, E)
    r = dijkstra(adj, "A")
    assert r["dist"] == {"A": 0, "B": 3, "C": 2, "D": 8, "E": 10, "F": 13}
    assert shortest_path(r["prev"], "A", "F") == ["A", "C", "B", "D", "E", "F"]


def test_dijkstra_disconnected_and_single():
    adj = build_adjacency(["A", "B", "C"], [("A", "B", 2)])
    r = dijkstra(adj, "A")
    assert r["dist"]["C"] == INF and shortest_path(r["prev"], "A", "C") == []
    assert dijkstra(build_adjacency(["A"], []), "A")["dist"] == {"A": 0}


def test_dijkstra_rejects_negative_weight():
    with pytest.raises(ValueError):
        dijkstra(build_adjacency(["A", "B"], [("A", "B", -1)]), "A")


def test_dijkstra_zero_weight_and_parallel_edges():
    adj = build_adjacency(["A", "B"], [("A", "B", 5), ("A", "B", 0)])
    assert dijkstra(adj, "A")["dist"]["B"] == 0


def test_dijkstra_random_vs_bellman_ford():
    rng = random.Random(9)
    for _ in range(30):
        n = rng.randint(2, 8)
        vs = list(range(n))
        es = [(rng.randrange(n), rng.randrange(n), rng.randint(0, 9)) for _ in range(rng.randint(0, 15))]
        dist = {v: INF for v in vs}
        dist[0] = 0
        for _ in range(n):
            for u, v, w in es:
                dist[u] = min(dist[u], dist[v] + w)
                dist[v] = min(dist[v], dist[u] + w)
        assert dijkstra(build_adjacency(vs, es), 0)["dist"] == dist


def test_kruskal_known():
    r = kruskal(V, E)
    assert r["total_weight"] == 13 and len(r["mst_edges"]) == 5 and r["connected"]


def test_kruskal_disconnected_gives_forest():
    r = kruskal(["A", "B", "C", "D"], [("A", "B", 1), ("C", "D", 2)])
    assert r["total_weight"] == 3 and not r["connected"]


def test_kruskal_edge_cases():
    assert kruskal(["A"], [])["connected"] and kruskal(["A"], [])["total_weight"] == 0
    assert kruskal(["A", "B"], [("A", "A", 1)])["mst_edges"] == []      # self-loop ignored
    assert kruskal(["A", "B"], [("A", "B", -3)])["total_weight"] == -3  # negative OK for Kruskal


def test_kruskal_random_vs_brute_force():
    rng = random.Random(4)
    for _ in range(25):
        n = rng.randint(2, 6)
        vs = list(range(n))
        es = [(rng.randrange(n), rng.randrange(n), rng.randint(1, 9)) for _ in range(rng.randint(1, 9))]
        best = None
        for combo in itertools.combinations(es, n - 1):
            uf = UnionFind(vs)
            if all(uf.union(u, v) for u, v, _ in combo):
                w = sum(c[2] for c in combo)
                best = w if best is None else min(best, w)
        r = kruskal(vs, es)
        if best is None:
            assert not r["connected"]
        else:
            assert r["connected"] and r["total_weight"] == best


def test_invalid_graphs():
    with pytest.raises(ValueError):
        build_adjacency(["A", "B"], [("A", "Z", 1)])
    with pytest.raises(ValueError):
        build_adjacency(["A", "A"], [])
    with pytest.raises(ValueError):
        build_adjacency(["A", "B"], [("A", "B", "heavy")])


def test_helpers():
    h = MinHeap()
    for x in [5, 1, 4, 2, 3]:
        h.push(x)
    assert [h.pop() for _ in range(5)] == [1, 2, 3, 4, 5]
    with pytest.raises(IndexError):
        h.pop()
    assert merge_sort_by([3, 1, 2], key=lambda x: x) == [1, 2, 3]
