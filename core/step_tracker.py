"""
step_tracker.py
---------------
Records what an algorithm does while it runs.

* Counters (comparisons, swaps, operations) are used by the Performance Analyzer.
* Steps (snapshots with a text description) are used by the visualizers.

Algorithms accept an optional `tracker`. If none is given they use NULL_TRACKER,
which does nothing, so normal runs and benchmarks stay fast.
Pattern used inside algorithms:   if t.recording: t.add("text", array=list(a))
(the `if` avoids copying the array when nobody is watching).
"""


class StepTracker:
    def __init__(self, record_steps=True):
        self.recording = record_steps
        self.steps = []
        self.comparisons = 0
        self.swaps = 0          # swaps or element moves/writes
        self.operations = 0     # other basic operations (multiplications, edge checks ...)

    def add(self, description, **state):
        if self.recording:
            self.steps.append({"description": description, **state})

    def compare(self, n=1):
        self.comparisons += n

    def swap(self, n=1):
        self.swaps += n

    def op(self, n=1):
        self.operations += n

    def total_operations(self):
        return self.comparisons + self.swaps + self.operations

    def summary(self):
        return {"comparisons": self.comparisons, "swaps": self.swaps,
                "operations": self.operations}


class NullTracker:
    """A tracker that ignores everything (used when no tracker is passed)."""
    recording = False

    def add(self, *a, **k): pass
    def compare(self, n=1): pass
    def swap(self, n=1): pass
    def op(self, n=1): pass


NULL_TRACKER = NullTracker()


def ensure(tracker):
    """Return the given tracker, or the do-nothing tracker if None."""
    return NULL_TRACKER if tracker is None else tracker
