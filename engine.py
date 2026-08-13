"""v2 — pillar 2: the diff. Desired vs state.

Desired state now lives in infra.yaml, so the program is data. One
dependency — a YAML parser — because parsing was never the interesting part.

    python engine.py plan   # say what would change, touch nothing

Compare desired against state and you get three sets: create, update, delete.
That is the whole of what a progress bar is hiding from you.
"""
import json, os, subprocess, sys, urllib.request
import yaml  # the one import: infra.yaml -> dict, one line, not a pillar

SUB = os.environ["AZURE_SUBSCRIPTION_ID"]
BASE = "https://management.azure.com"
STATE_FILE = "state.json"

def get_token():
    return subprocess.check_output(
        ["az", "account", "get-access-token", "--query", "accessToken", "-o", "tsv"],
        text=True).strip()

def call(method, url, body=None):
    req = urllib.request.Request(url, method=method,
        data=json.dumps(body).encode() if body is not None else None,
        headers={"Authorization": "Bearer " + TOKEN, "Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        return resp.status, json.loads(resp.read() or b"null")

def url_for(res):
    return f"{BASE}/subscriptions/{SUB}/resourcegroups/{res['name']}?api-version=2024-03-01"

# ---- pillar 1: state — what we THINK exists --------------------------------

def load_state():
    return json.load(open(STATE_FILE)) if os.path.exists(STATE_FILE) else {}

def save_state(state):
    json.dump(state, open(STATE_FILE, "w"), indent=2)

# ---- pillar 2: the diff — desired vs state ---------------------------------

def diff(desired, state):
    creates = [k for k in desired if k not in state]
    deletes = [k for k in state if k not in desired]
    updates = [k for k in desired if k in state
               and desired[k]["properties"] != state[k]["saved"]]
    return creates, updates, deletes

def show(creates, updates, deletes):
    for k in creates: print(f"  + create {k}")
    for k in updates: print(f"  ~ update {k}")
    for k in deletes: print(f"  - delete {k}")
    if not (creates or updates or deletes):
        print("  no changes.")

# ----------------------------------------------------------------------------

TOKEN = get_token()
desired = yaml.safe_load(open("infra.yaml"))["resources"]
verb = sys.argv[1] if len(sys.argv) > 1 else "plan"
state = load_state()

creates, updates, deletes = diff(desired, state)
show(creates, updates, deletes)

if verb == "up":  # reconciliation is the next pillar; for now, creates only
    for key in creates:
        call("PUT", url_for(desired[key]), desired[key]["properties"])
        state[key] = {"res": desired[key], "saved": desired[key]["properties"]}
        save_state(state)
