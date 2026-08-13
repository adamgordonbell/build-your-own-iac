"""v0 — the cloud is just a REST API.

No SDK, no framework. A bearer token and one PUT.
Run it twice: PUT is an upsert, so nothing breaks. So why do we need
anything more than this?

    python engine.py
"""
import json, os, subprocess, urllib.request

SUB = os.environ["AZURE_SUBSCRIPTION_ID"]
BASE = "https://management.azure.com"

def get_token():
    return subprocess.check_output(
        ["az", "account", "get-access-token", "--query", "accessToken", "-o", "tsv"],
        text=True).strip()

def call(method, url, body=None):
    print(f"{method} {url}")
    if body is not None:
        print(f"  body: {json.dumps(body)}")
    req = urllib.request.Request(url, method=method,
        data=json.dumps(body).encode() if body is not None else None,
        headers={"Authorization": "Bearer " + TOKEN, "Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        print(f"  -> {resp.status}")
        return json.loads(resp.read() or b"null")

TOKEN = get_token()

call("PUT",
     f"{BASE}/subscriptions/{SUB}/resourcegroups/byoiac-demo?api-version=2024-03-01",
     {"location": "eastus", "tags": {"env": "demo", "talk": "kcdc"}})
