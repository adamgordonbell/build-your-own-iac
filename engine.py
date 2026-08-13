"""v3 — pillar 3: reconciliation. A working IaC tool.

Raw Azure REST, no SDK, no frameworks: every ARM resource is just
PUT / GET / DELETE on a resource ID. The rest is a diff loop.

    python engine.py plan | up | destroy

State, diff, reconcile. That is the whole idea, and it fits on a slide.
"""
import json, os, subprocess, sys, urllib.error, urllib.request
import yaml  # the one import: infra.yaml -> dict, one line, not a pillar

SUB = os.environ["AZURE_SUBSCRIPTION_ID"]
BASE = "https://management.azure.com"
STATE_FILE = "state.json"

# ---- the cloud is just a REST API ------------------------------------------

def get_token():
    return subprocess.check_output(
        ["az", "account", "get-access-token", "--query", "accessToken", "-o", "tsv"],
        text=True).strip()

def call(method, url, body=None):
    req = urllib.request.Request(url, method=method,
        data=json.dumps(body).encode() if body is not None else None,
        headers={"Authorization": "Bearer " + TOKEN, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read() or b"null")
    except urllib.error.HTTPError as err:
        if err.code == 404:
            return 404, None
        raise SystemExit(f"{method} {url}\n  -> {err.code}: {err.read().decode()[:300]}")

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

# ---- pillar 3: reconciliation — make the diff true -------------------------

def apply(desired, state, creates, updates, deletes):
    for key in deletes:
        print(f"  - {key}")
        call("DELETE", url_for(state[key]["res"]))
        del state[key]
        save_state(state)               # save as we go, so partial failure
    for key in creates + updates:       # leaves state matching reality
        res = desired[key]
        print(f"  {'+' if key in creates else '~'} {key}")
        call("PUT", url_for(res), res["properties"])
        state[key] = {"res": res, "saved": res["properties"]}
        save_state(state)

# ----------------------------------------------------------------------------

def main():
    global TOKEN
    TOKEN = get_token()
    desired = yaml.safe_load(open("infra.yaml"))["resources"]
    verb = sys.argv[1] if len(sys.argv) > 1 else "plan"
    state = load_state()
    if verb == "destroy":
        desired = {}
    creates, updates, deletes = diff(desired, state)
    show(creates, updates, deletes)
    if verb in ("up", "destroy"):
        apply(desired, state, creates, updates, deletes)

if __name__ == "__main__":
    main()
