"""v5 — the cliff.

    python engine.py plan | up | destroy | refresh

`refresh` asks the cloud what is ACTUALLY there. And that is where the
uniform API stops helping. We PUT 4 fields at the storage account; the GET
answers with 48. A naive diff would try to "fix" 44 fields it does not own —
including ones it is not allowed to write.

The fix, for exactly one resource type, is OWNED below: per-property,
per-resource-type knowledge. Multiply by ~2,000 ARM types, then by every
cloud. The loop was 100 lines. The schemas are the millions.
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

# ---- the cliff: the API returns ~50 fields; we own a handful ---------------

OWNED = {  # per resource type: the properties that are OURS to manage
    "Microsoft.Resources/resourceGroups": ["location", "tags"],
    "Microsoft.Storage/storageAccounts": ["location", "tags", "sku", "kind"],
}

def owned(res):  # our declared properties, minus anything not ours to manage
    return {k: v for k, v in res["properties"].items() if k in OWNED[res["type"]]}

def project(shape, actual):  # trim the cloud's answer to the shape we sent
    if isinstance(shape, dict) and isinstance(actual, dict):
        return {k: project(v, actual[k]) for k, v in shape.items() if k in actual}
    return actual                       # (sku comes back with a tier we never sent)

# ---- pillar 2: the diff — desired vs state ---------------------------------

def diff(desired, state):
    creates = [k for k in desired if k not in state]
    deletes = [k for k in state if k not in desired]
    updates = [k for k in desired if k in state
               and owned(desired[k]) != state[k]["saved"]]
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
            state[key] = {"res": res, "saved": owned(res)}
            save_state(state)

# ---- drift: ask the cloud what is ACTUALLY there ---------------------------

def refresh(state):
    for key in state:
        res = state[key]["res"]
        _, actual = call("GET", url_for(res))
        print(f"  = {key}: cloud returned {len(actual)} top-level fields; "
              f"we own {len(OWNED[res['type']])}")
        state[key]["saved"] = project(owned(res), actual)
    save_state(state)

# ----------------------------------------------------------------------------

def main():
    global TOKEN
    TOKEN = get_token()
    desired = yaml.safe_load(open("infra.yaml"))["resources"]
    verb = sys.argv[1] if len(sys.argv) > 1 else "plan"
    state = load_state()
    if verb == "refresh":
        refresh(state)
        return
    if verb == "destroy":
        desired = {}
    creates, updates, deletes = diff(desired, state)
    show(creates, updates, deletes)
    if verb in ("up", "destroy"):
        apply(desired, state, creates, updates, deletes)

if __name__ == "__main__":
    main()
