"""v4 — hard problem: dependency graphs (and eventual consistency, free).

A storage account has to be created *after* its resource group, and deleted
*before* it. So the resources are a graph, and the engine walks it in
topological order — parents first on the way up, children first on the way down.

    python engine.py plan | up | destroy

The storage account also answers 202 Accepted, not 200 OK: "working on it".
Real clouds are eventually consistent, so the engine polls until the resource
says provisioningState: Succeeded.
"""
import json, os, subprocess, sys, time, urllib.error, urllib.request
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
    if res["type"] == "Microsoft.Resources/resourceGroups":
        return f"{BASE}/subscriptions/{SUB}/resourcegroups/{res['name']}?api-version=2024-03-01"
    return (f"{BASE}/subscriptions/{SUB}/resourceGroups/{res['resourceGroup']}"
            f"/providers/{res['type']}/{res['name']}?api-version=2023-05-01")

def wait_ready(res):  # 201/202 = "working on it" — poll until the cloud is done
    while True:
        code, actual = call("GET", url_for(res))
        if code != 404 and (actual or {}).get("properties", {}).get(
                "provisioningState") == "Succeeded":
            return
        time.sleep(2)

# ---- dependency graph: parents before children -----------------------------

def ordered(resources):  # depth-first topological sort
    done, order = set(), []
    def visit(key):
        if key not in done:
            done.add(key)
            for dep in resources[key].get("dependsOn", []):
                visit(dep)
            order.append(key)
    for key in resources:
        visit(key)
    return order

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
    for key in reversed(ordered({k: state[k]["res"] for k in state})):
        if key in deletes:              # children first on the way down
            print(f"  - {key}")
            call("DELETE", url_for(state[key]["res"]))
            del state[key]
            save_state(state)           # save as we go, so partial failure
    for key in ordered(desired):        # leaves state matching reality
        if key in creates or key in updates:
            res = desired[key]
            print(f"  {'+' if key in creates else '~'} {key}")
            call("PUT", url_for(res), res["properties"])
            wait_ready(res)
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
