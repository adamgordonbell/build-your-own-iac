"""The script you write instead of clicking the portal.

I have a web page. It needs to be on the internet. I could click through the
Azure portal for ten minutes — but I'm smarter than that, so I script it.
Every `az` command is one HTTP request, so here they are, in order, with no
SDK and no framework: a bearer token and four PUTs.

    export AZURE_SUBSCRIPTION_ID=$(az account show --query id -o tsv)
    python deploy.py

Run it, the page is live. So why does anybody need Terraform?
"""
import json, os, subprocess, time, urllib.request

SUB = os.environ["AZURE_SUBSCRIPTION_ID"]
ARM = "https://management.azure.com"
RG, ACCOUNT, CONTAINER, BLOB = "byoiac-demo", "byoiacdemo2026", "files", "hello.html"

# need a token — borrow az's, rather than rolling our own OAuth
TOKEN = subprocess.check_output(
    ["az", "account", "get-access-token", "--query", "accessToken", "-o", "tsv"],
    text=True).strip()

def call(method, url, body=None):
    print(f"{method} {url.split('?')[0]}")
    req = urllib.request.Request(url, method=method,
        data=json.dumps(body).encode() if body is not None else None,
        headers={"Authorization": "Bearer " + TOKEN, "Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        print(f"  -> {resp.status}")
        return json.loads(resp.read() or b"null")

# 1. the resource group
call("PUT", f"{ARM}/subscriptions/{SUB}/resourcegroups/{RG}?api-version=2024-03-01",
     {"location": "eastus", "tags": {"env": "demo", "talk": "kcdc"}})

# 2. the storage account
call("PUT", f"{ARM}/subscriptions/{SUB}/resourceGroups/{RG}"
     f"/providers/Microsoft.Storage/storageAccounts/{ACCOUNT}?api-version=2023-05-01",
     {"location": "eastus", "sku": {"name": "Standard_LRS"}, "kind": "StorageV2",
      "tags": {"env": "demo"}, "properties": {"allowBlobPublicAccess": True}})

# storage takes a while. how long? ¯\_(ツ)_/¯ 20s is usually enough
print("sleeping 20s for the storage account...")
time.sleep(20)

# 3. the container — still ARM, just a deeper URL
call("PUT", f"{ARM}/subscriptions/{SUB}/resourceGroups/{RG}"
     f"/providers/Microsoft.Storage/storageAccounts/{ACCOUNT}"
     f"/blobServices/default/containers/{CONTAINER}?api-version=2023-05-01",
     {"properties": {"publicAccess": "Blob"}})

# 4. the file itself. blobs are the data plane: a different API, different auth,
#    so ask the management plane to sign us a SAS. still a PUT, though.
sas = call("POST", f"{ARM}/subscriptions/{SUB}/resourceGroups/{RG}"
           f"/providers/Microsoft.Storage/storageAccounts/{ACCOUNT}"
           f"/listServiceSas?api-version=2023-05-01",
           {"canonicalizedResource": f"/blob/{ACCOUNT}/{CONTAINER}",
            "signedResource": "c", "signedPermission": "rcwd", "signedProtocol": "https",
            "signedExpiry": time.strftime("%Y-%m-%dT%H:%M:%SZ",
                                          time.gmtime(time.time() + 3600))})["serviceSasToken"]

PAGE = "<h1>Deployed by one dumb script</h1><p>KCDC 2026 - Build Your Own IaC</p>"
blob_url = f"https://{ACCOUNT}.blob.core.windows.net/{CONTAINER}/{BLOB}"
print(f"PUT {blob_url}")
req = urllib.request.Request(f"{blob_url}?{sas}", method="PUT", data=PAGE.encode(),
    headers={"x-ms-version": "2021-08-06", "x-ms-blob-type": "BlockBlob",
             "Content-Type": "text/html"})
with urllib.request.urlopen(req) as resp:
    print(f"  -> {resp.status}")

print(f"\nyour page: {blob_url}")
