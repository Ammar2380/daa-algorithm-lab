"""Generate docs/algorithm_reference.md from core/complexity.py (run from the project root)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.complexity import ALGORITHM_INFO, CATEGORY_ORDER

out = ["# Algorithm Reference\n", "Generated from `core/complexity.py`, the same data the app displays.\n"]
summary = ["| Algorithm | Best | Average | Worst | Space |", "|---|---|---|---|---|"]
for cat in CATEGORY_ORDER:
    for i in [x for x in ALGORITHM_INFO.values() if x["category"] == cat]:
        summary.append(f"| {i['name']} | {i['best'].split(' - ')[0]} | {i['average'].split(' - ')[0]} | "
                       f"{i['worst'].split(' - ')[0]} | {i['space'].split(' (')[0].split(' for')[0]} |")
out += ["## Complexity summary\n", "\n".join(summary) + "\n"]
for cat in CATEGORY_ORDER:
    out.append(f"\n## {cat}\n")
    for i in [x for x in ALGORITHM_INFO.values() if x["category"] == cat]:
        out.append(f"### {i['name']}\n")
        out.append(f"1. **Problem definition:** {i['problem']}")
        out.append(f"2. **Input and output:** {i['input_output']}")
        out.append("3. **Step-by-step explanation:**\n" + "\n".join(f"   - {s}" for s in i["how_it_works"]))
        out.append("4. **Pseudocode:**\n\n```text\n" + i["pseudocode"] + "\n```")
        out.append(f"5. **Python implementation:** `{i['function']}`")
        out.append(f"6. **Best-case time:** {i['best']}")
        out.append(f"7. **Average-case time:** {i['average']}")
        out.append(f"8. **Worst-case time:** {i['worst']}")
        out.append(f"9. **Auxiliary space:** {i['space']}")
        out.append(f"10. **Real-world applications:** {i['application']}")
        out.append(f"11. **Example execution:** {i['example']}")
        out.append(f"\n*Notes:* {i['notes']}\n")
Path("docs/algorithm_reference.md").write_text("\n".join(out), encoding="utf-8")
print("written docs/algorithm_reference.md")
