import json, csv
from collections import defaultdict

with open("lab-1.0.2-shared-container/api/data/submissions.json") as f:
    data = json.load(f)

by_period = defaultdict(list)
for entry in data.values():
    passed = sum([
        1,                                 # Assume L1.0.1: complete
        1,                                        # L1.0.2: submitted
        1 if entry.get("lab_103") else 0,         # L1.0.3: complete
    ])
    by_period[entry.get("period", "unknown")].append({
        "last_name":         entry.get("last_name", "?"),
        "first_name":        entry.get("first_name", "?"),
        "username":          entry.get("username", "?"),
        "period":            entry.get("period", "?"),
        "lab_id":            "lab_1_0",
        "passed_assertions": passed,
        "failed_assertions": 3 - passed,
        "grade_percentage":  round(passed / 3 * 100, 1),
    })

for period, rows in sorted(by_period.items()):
    rows.sort(key=lambda r: (r["last_name"].lower(), r["first_name"].lower()))
    filename = f"grades_report_period{period}.csv"
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {filename} — {len(rows)} students")