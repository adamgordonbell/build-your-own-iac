"""v1 — pillar 1: state. What we THINK exists.

PUT is an upsert, so creating is safe. But an IaC tool has to know what it
made, or it can never clean up after itself. So: write down what we created.

    python engine.py

state.json is that memory. It also shows the crack: state is a *belief*.
Rename a resource and we forget the old one. Delete it in the portal and we
still think it's there.
"""
import json, os, subprocess, urllib.request

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

# ----------------------------------------------------------------------------

DESIRED = {  # still hardcoded — the input language comes next
    "rg": {"type": "Microsoft.Resources/resourceGroups", "name": "byoiac-demo",
           "properties": {"location": "eastus", "tags": {"env": "demo", "talk": "kcdc"}}},
}

TOKEN = get_token()
state = load_state()

for key, res in DESIRED.items():
    if key in state:
        print(f"  = {key} already in state — skipping")
        continue
    print(f"  + {key} {res['name']}")
    call("PUT", url_for(res), res["properties"])
    state[key] = {"res": res}
    save_state(state)
