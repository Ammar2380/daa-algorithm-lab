"""Run all benchmark suites and write docs/benchmark_results.md (measured on THIS machine)."""
import platform
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import pandas as pd
from core.benchmark import SUITES, run_suite

REPEATS = 5
lines = [f"Machine: Python {platform.python_version()} on {platform.system()} {platform.machine()}; "
         f"{REPEATS} repetitions, median time, seed 42.\n"]
for name, suite in SUITES.items():
    scenario = suite.scenarios[0]
    rows = run_suite(suite, scenario, suite.default_sizes, REPEATS, 42)
    df = pd.DataFrame(rows)
    table = df.pivot(index="n", columns="Algorithm", values="Median time (ms)").round(4)
    ops = df.pivot(index="n", columns="Algorithm", values="Total operations")
    lines.append(f"\n#### {name} - scenario: {scenario}\n\nMedian time (ms):\n\n{table.to_markdown()}\n\n"
                 f"Total operations:\n\n{ops.to_markdown()}\n")
    print("done", name, flush=True)
# Extra: sorting scenarios at n = 1000
s = SUITES["Sorting"]
extra = {sc: {r["Algorithm"]: r["Comparisons"] for r in run_suite(s, sc, [1000], 1, 42)} for sc in s.scenarios}
lines.append("\n#### Sorting at n = 1000: comparisons by input scenario\n\n" +
             pd.DataFrame(extra).to_markdown() + "\n")
Path("docs/benchmark_results.md").write_text("\n".join(lines), encoding="utf-8")
