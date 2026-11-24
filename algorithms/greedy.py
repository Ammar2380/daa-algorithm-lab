"""
greedy.py - Activity Selection, Fractional Knapsack, Huffman Coding.
"""
from algorithms.data_structures import MinHeap, merge_sort_by
from core.step_tracker import ensure


# ---------------------------------------------------------------- Activity selection
def activity_selection(activities, tracker=None):
    """activities: list of (start, finish). Greedy rule: always take the compatible
    activity that finishes earliest. Returns dict(selected=[indices], order=[indices])."""
    t = ensure(tracker)
    for a in activities:
        if len(a) != 2 or a[1] < a[0]:
            raise ValueError(f"Invalid activity {a}: need (start, finish) with finish >= start.")
    order = merge_sort_by(range(len(activities)), key=lambda i: activities[i][1])
    selected, last_finish = [], None
    if t.recording:
        t.add("Sort activities by finishing time.", order=order, selected=[], rejected=[], current=None)
    rejected = []
    for idx in order:
        start, finish = activities[idx]
        t.compare()
        if last_finish is None or start >= last_finish:
            note = ("it is the first one" if last_finish is None
                    else f"it starts at {start}, not before the last finish time {last_finish}")
            selected.append(idx)
            last_finish = finish
            if t.recording:
                t.add(f"Activity {idx} ({start}-{finish}): {note}, so SELECT it.", order=order,
                      selected=list(selected), rejected=list(rejected), current=idx)
        else:
            rejected.append(idx)
            if t.recording:
                t.add(f"Activity {idx} ({start}-{finish}) starts before the last selected one finishes "
                      f"({last_finish}): SKIP it.", order=order, selected=list(selected),
                      rejected=list(rejected), current=idx)
    return {"selected": selected, "order": list(order)}


# ---------------------------------------------------------------- Fractional knapsack
def fractional_knapsack(items, capacity, tracker=None):
    """items: list of (value, weight). Returns dict(total_value, taken=[(index, fraction)], order)."""
    t = ensure(tracker)
    if capacity < 0:
        raise ValueError("Capacity cannot be negative.")
    for v, w in items:
        if w <= 0 or v < 0:
            raise ValueError(f"Invalid item {(v, w)}: weight must be > 0 and value >= 0.")
    order = merge_sort_by(range(len(items)), key=lambda i: -(items[i][0] / items[i][1]))
    remaining, total, taken = capacity, 0.0, []
    if t.recording:
        t.add("Sort items by value/weight ratio (highest first).", order=order, taken=[],
              remaining=remaining, total=0.0, current=None)
    for idx in order:
        if remaining <= 0:
            break
        v, w = items[idx]
        t.compare()
        if w <= remaining:
            fraction = 1.0
            text = f"Item {idx} (value {v}, weight {w}) fits completely: take all of it."
        else:
            fraction = remaining / w
            text = (f"Item {idx} (value {v}, weight {w}) does not fit: take fraction "
                    f"{remaining}/{w} = {fraction:.3f}.")
        remaining -= w * fraction
        total += v * fraction
        taken.append((idx, fraction))
        if t.recording:
            t.add(text, order=order, taken=list(taken), remaining=remaining, total=total, current=idx)
    return {"total_value": total, "taken": taken, "order": list(order)}


# ---------------------------------------------------------------- Huffman coding
class HuffmanNode:
    __slots__ = ("char", "freq", "left", "right")

    def __init__(self, char, freq, left=None, right=None):
        self.char, self.freq, self.left, self.right = char, freq, left, right

    def is_leaf(self):
        return self.left is None and self.right is None


def _label(node):
    return node.char if node.is_leaf() else f"[{node.freq}]"


def huffman_coding(text, tracker=None):
    """Build the Huffman tree for `text`. Returns dict(codes, encoded, tree, freq)."""
    t = ensure(tracker)
    if not isinstance(text, str):
        raise TypeError("Input must be a string.")
    if text == "":
        raise ValueError("Text must not be empty.")
    freq = {}
    for ch in text:
        freq[ch] = freq.get(ch, 0) + 1
    heap, counter = MinHeap(), 0
    for ch, f in freq.items():
        heap.push((f, counter, HuffmanNode(ch, f)))
        counter += 1
    if t.recording:
        t.add("Create one leaf per character and put all in a min-heap.",
              forest=sorted((n.freq, _label(n)) for _, _, n in heap.data))
    if len(heap) == 1:                      # only one distinct symbol
        root = heap.pop()[2]
        codes = {root.char: "0"}
    else:
        while len(heap) > 1:
            f1, _, a = heap.pop()
            f2, _, b = heap.pop()
            t.compare()
            parent = HuffmanNode(None, f1 + f2, a, b)
            heap.push((parent.freq, counter, parent))
            counter += 1
            if t.recording:
                t.add(f"Merge the two smallest: {_label(a)} ({f1}) + {_label(b)} ({f2}) "
                      f"-> new node with frequency {f1 + f2}.",
                      forest=sorted((n.freq, _label(n)) for _, _, n in heap.data), merged=parent)
        root = heap.pop()[2]
        codes = {}
        stack = [(root, "")]
        while stack:
            node, prefix = stack.pop()
            if node.is_leaf():
                codes[node.char] = prefix
            else:
                stack.append((node.right, prefix + "1"))
                stack.append((node.left, prefix + "0"))
    encoded = "".join(codes[ch] for ch in text)
    if t.recording:
        t.add(f"Tree finished. Original = {8 * len(text)} bits, encoded = {len(encoded)} bits.",
              forest=[(root.freq, _label(root))], merged=root)
    return {"codes": codes, "encoded": encoded, "tree": root, "freq": freq}


def huffman_decode(encoded, tree):
    """Decode a bit string using the Huffman tree (used to verify the coding)."""
    if tree.is_leaf():
        return tree.char * len(encoded)
    out, node = [], tree
    for bit in encoded:
        node = node.left if bit == "0" else node.right
        if node.is_leaf():
            out.append(node.char)
            node = tree
    return "".join(out)
