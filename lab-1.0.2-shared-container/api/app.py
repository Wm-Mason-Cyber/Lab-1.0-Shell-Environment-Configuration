from flask import Flask, request, jsonify, render_template_string
import json, os, datetime

app = Flask(__name__)
DATA_FILE = "/data/submissions.json"


def load():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            return json.load(f)
    return {}


def save(data):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


@app.route("/lab-1-0-2", methods=["POST"])
def receive_102():
    body = request.get_json(force=True)
    username = body.get("username", "unknown")
    data = load()
    entry = data.get(username, {})
    entry.update({
        "username": username,
        "first_name": body.get("first_name", entry.get("first_name", "?")),
        "last_name": body.get("last_name", entry.get("last_name", "?")),
        "period": body.get("period", "?"),
        "timestamp_102": body.get("timestamp", datetime.datetime.now().isoformat()),
        "lab_103": entry.get("lab_103", False),
    })
    data[username] = entry
    save(data)
    return jsonify({"status": "ok", "message": f"Received! Welcome, {username}."})


@app.route("/lab-1-0-3", methods=["POST"])
def receive_103():
    body = request.get_json(force=True)
    username = body.get("username", "unknown")
    data = load()
    entry = data.get(username, {"username": username, "period": body.get("period", "?"), "lab_103": False})
    entry["lab_103"] = True
    entry["timestamp_103"] = datetime.datetime.now().isoformat()
    entry["syscheck_output"] = body.get("output", "")
    data[username] = entry
    save(data)
    return jsonify({"status": "ok", "message": f"Lab 1.0.3 recorded for {username}!"})


DASHBOARD = """<!DOCTYPE html>
<html>
<head>
  <title>Lab 1.0 Submissions</title>
  <meta http-equiv="refresh" content="10">
  <style>
    body { font-family: monospace; background: #0d1117; color: #e6edf3; padding: 2rem; }
    h1 { color: #58a6ff; }
    p.count { color: #8b949e; font-size: 0.9em; margin-top: 0.5rem; }
    table { border-collapse: collapse; width: 100%; margin-top: 1rem; }
    th { background: #161b22; color: #8b949e; padding: 8px 12px; text-align: left; border-bottom: 2px solid #30363d; }
    td { padding: 8px 12px; border-bottom: 1px solid #21262d; }
    .check { color: #3fb950; font-weight: bold; }
    .pending { color: #6e7681; }
    .ts { color: #8b949e; font-size: 0.85em; }
  </style>
</head>
<body>
  <h1>Lab 1.0 — Live Submissions</h1>
  <p class="count">{{ count }} student(s) submitted &nbsp;|&nbsp; auto-refreshes every 10s</p>
  <table>
    <tr>
      <th>Username</th>
      <th>Name</th>
      <th>Period</th>
      <th>1.0.2 Submitted At</th>
      <th>1.0.3 Complete</th>
    </tr>
    {% for u in students %}
    <tr>
      <td>{{ u.username }}</td>
      <td>{{ u.get("last_name", "?") }}, {{ u.get("first_name", "?") }}</td>
      <td>{{ u.period }}</td>
      <td class="ts">{{ u.get("timestamp_102", "—") }}</td>
      <td>{% if u.lab_103 %}<span class="check">&#10003;</span>{% else %}<span class="pending">—</span>{% endif %}</td>
    </tr>
    {% endfor %}
  </table>
</body>
</html>"""


@app.route("/")
def dashboard():
    data = load()
    students = sorted(data.values(), key=lambda x: (x.get("period", ""), x.get("last_name", "").lower(), x.get("first_name", "").lower()))
    return render_template_string(DASHBOARD, students=students, count=len(students))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
