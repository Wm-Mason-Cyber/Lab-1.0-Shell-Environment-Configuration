# Teacher Setup — Lab 1.0

**Audience:** Instructor only  
**Time Required:** ~10 minutes pre-class setup

---

## Prerequisites

Your host machine (the classroom server or your laptop) needs:

- **Docker** and **Docker Compose** installed
- Reachable on the classroom LAN — find your IP with:
  ```shell
  ip addr show | grep "inet " | grep -v "127.0.0.1"
  ```
- Port `8080` not blocked by a local firewall (`ufw allow 8080` if needed)

Students need:
- `curl` installed (present by default on Debian/Fedora)
- `ping` installed (present by default)
- A terminal with `bash` or `zsh`

---

## Pre-Class Setup

### 1. Start the API Container

```shell
cd lab-1.0.2-shared-container/api
docker compose up -d
```

Verify it's running:

```shell
docker compose ps
curl http://localhost:8080/
```

The dashboard page should load. Open it in a browser to display on the projector: `http://<your-ip>:8080`

### 2. Give Students the IP Address

Tell students (or write on the board):

```
TARGET_GATEWAY = http://<your-ip>:8080
```

This is the value they will `export` in L1.0.2 Step 2.

### 3. Distribute the Submission Script (Optional)

Students can copy the `lab-1.0-api-send` script from this repo to their machines, or copy-paste it from the LESSON.md. Either works. If distributing via shared drive or USB:

```shell
cp lab-1.0.2-shared-container/lab-1.0-api-send /path/to/shared/drive/
```

---

## During the Lab

### L1.0.1 — No Action Required

L1.0.1 is entirely local to each student's terminal. No setup, no grading infrastructure. Students take a screenshot if you want a participation artifact, but the LESSON.md explicitly marks this section as ephemeral.

### L1.0.2 — Monitor the Dashboard

Keep the browser dashboard open on the projector: `http://<your-ip>:8080`

It auto-refreshes every 10 seconds. As students submit, their names and usernames appear in the table sorted by period then alphabetically by last name. The **1.0.3 Complete** column starts as `—` for everyone and fills in as students finish L1.0.3.

If a student says their submission didn't appear:
- Have them run `printenv | grep TARGET_GATEWAY` to verify the variable is set correctly
- Check they ran `chmod +x lab-1.0-api-send` before executing it
- Check they used `./lab-1.0-api-send` or the full path (or it's in their PATH)

### L1.0.3 — No Additional Setup

L1.0.3 submits to the same API container using the `/lab-1-0-3` endpoint. Students need `$TARGET_GATEWAY` and `$CLASS_PERIOD` exported before running the submission commands. Both should be set if they completed L1.0.2 and sourced their `.bashrc`.

---

## Grading

### What Counts as Complete

| Section | Completion Criteria |
|---------|---------------------|
| L1.0.1 | Participation / screenshot (no automated check) |
| L1.0.2 | Username appears in dashboard table |
| L1.0.3 | ✓ checkmark appears in the "1.0.3 Complete" column |

### Reading the Raw Data

Submissions are stored as JSON at `lab-1.0.2-shared-container/api/data/submissions.json` on your host machine. This file is human-readable and contains every submission for the period:

```json
{
  "jsmith": {
    "username": "jsmith",
    "first_name": "Jane",
    "last_name": "Smith",
    "period": "1",
    "timestamp_102": "2026-06-01T09:14:22",
    "lab_103": true,
    "timestamp_103": "2026-06-01T09:31:05"
  }
}
```

To get a quick count of who completed each section:

```shell
# Total L1.0.2 submissions
cat lab-1.0.2-shared-container/api/data/submissions.json | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'1.0.2: {len(d)} students')"

# Who completed L1.0.3
cat lab-1.0.2-shared-container/api/data/submissions.json | python3 -c "import json,sys; d=json.load(sys.stdin); done=[u for u,v in d.items() if v.get('lab_103')]; print(f'1.0.3 complete ({len(done)}): {done}')"
```

### Grade Book Export

Run this from the repo root to produce one CSV per class period, sorted by last name:

```shell
python3 - <<'EOF'
import json, csv
from collections import defaultdict

with open("lab-1.0.2-shared-container/api/data/submissions.json") as f:
    data = json.load(f)

by_period = defaultdict(list)
for entry in data.values():
    passed = sum([
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
        "failed_assertions": 2 - passed,
        "grade_percentage":  round(passed / 2 * 100, 1),
    })

for period, rows in sorted(by_period.items()):
    rows.sort(key=lambda r: (r["last_name"].lower(), r["first_name"].lower()))
    filename = f"grades_report_period{period}.csv"
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {filename} — {len(rows)} students")
EOF
```

---

## Between-Period Reset

The API container keeps running between periods. To clear submissions for the next period:

```shell
rm lab-1.0.2-shared-container/api/data/submissions.json
```

The container will start fresh on the next POST — no restart needed.

If you want to preserve each period's data before clearing:

```shell
cp lab-1.0.2-shared-container/api/data/submissions.json \
   lab-1.0.2-shared-container/api/data/submissions_period1.json
rm lab-1.0.2-shared-container/api/data/submissions.json
```

---

## Teardown

At the end of the day:

```shell
cd lab-1.0.2-shared-container/api
docker compose down
```

Data persists in `./data/` on your host after the container stops. The container image stays cached for fast startup next time.

To fully clean up images and volumes:

```shell
docker compose down --rmi local --volumes
```

---

## Troubleshooting

**"Port 8080 already in use"**  
Another process holds 8080. Find it: `sudo lsof -i :8080`. Kill it or change the port in `docker-compose.yml` and LESSON.md.

**"Students can ping the IP but can't reach port 8080"**  
Check firewall: `sudo ufw status`. Allow the port: `sudo ufw allow 8080/tcp`.

**"Dashboard shows no submissions after students ran the script"**  
The `data/` directory may not exist yet or have wrong permissions. Check: `ls -la lab-1.0.2-shared-container/api/data/`. The container creates it automatically on first POST, but if it was created by root (from a previous `docker compose` run), the container may lack write permission. Fix: `sudo chown -R $USER:$USER lab-1.0.2-shared-container/api/data/`.

**"Student broke their PATH"**  
Direct them to the Emergency Troubleshooting section at the bottom of the L1.0.3 LESSON.md. The recovery command restores a working PATH for the current terminal session without touching any files.
