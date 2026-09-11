---
theme: default
title: Build Your Own IaC
info: |
  KCDC 2026 — Demystifying the Magic: Let's Build an IaC Tool from Scratch.
  One scenario, start to finish: a page that needs to be on the internet, and
  what happens to the script that puts it there. Every terminal output is a
  real transcript captured against Azure (2026-08-13, refreshed 2026-08-31).
highlighter: shiki
colorSchema: both

mdc: true
lineNumbers: false
drawings:
  persist: false
routeAlias: I_1
background: ./images/title-graph-bg.png
class: title-cover
---

<style>
.slidev-layout.title-cover { color: #f4f6fb !important; }
.slidev-layout.title-cover::before { content:''; position:absolute; inset:0; background:linear-gradient(90deg, rgba(7,10,15,0.72) 0%, rgba(7,10,15,0.36) 45%, rgba(7,10,15,0) 72%); pointer-events:none; z-index:0; }
.slidev-layout.title-cover h1 { position:relative; z-index:1; color:#ffffff !important; font-weight:700; -webkit-text-fill-color:#ffffff; }
.slidev-layout.title-cover h2 { position:relative; z-index:1; color:#cdd7ea !important; font-weight:400; -webkit-text-fill-color:#cdd7ea; }
</style>

# Build Your Own IaC

## Demystifying the Magic

<div class="abs-bl m-6 text-sm" style="color:#aeb9cc;z-index:2;">KCDC 2026 · Adam Gordon Bell · Pulumi</div>

<div class="absolute bottom-6 right-6 text-center" style="z-index:2;">
<img src="./images/adamgordonbell-qr.png" alt="adamgordonbell.com" style="width:88px;height:88px;border-radius:6px;" />
<div class="text-xs mt-1" style="color:#aeb9cc;">adamgordonbell.com</div>
</div>

<!--
- We want to put an HTML file on the web, using Azure.
- ▶ pre-stage: `az login` · export sub id · `rm -f state.json state.lock` · run from repo root (`src/` folders)
-->

---
routeAlias: I_1b
layout: center
---

<style>
.byox { --am:#f59e0b; --bl:#3b82f6; text-align:center; line-height:1.02; max-width:960px; margin:0 auto; }
.byox span { display:inline-block; margin:.14em .36em; white-space:nowrap; font-weight:600; background:none; border:none; }
.byox .am { color:var(--am); }
.byox .bl { color:var(--bl); }
.byox .d1{opacity:.9} .byox .d2{opacity:.62} .byox .d3{opacity:.42}
.byox .hero { color:var(--am); font-weight:800; border-bottom:3px solid var(--am); }
</style>

# Build your own *anything*

<div class="byox mt-5" style="font-size:1rem">
<span class="hero" style="font-size:2.3em">an IaC tool</span>
<span class="bl" style="font-size:1.6em">a shell</span>
<span class="d1" style="font-size:2em">a database</span>
<span class="d2" style="font-size:1.25em">git</span>
<span class="am" style="font-size:1.5em">a compiler</span>
<span class="d1" style="font-size:2.2em">an operating system</span>
<span class="d3" style="font-size:1.1em">a regex engine</span>
<span class="bl" style="font-size:1.35em">a ray tracer</span>
<span class="d2" style="font-size:1.65em">a text editor</span>
<span class="d1" style="font-size:1.2em">a garbage collector</span>
<span class="am" style="font-size:1.85em">a virtual machine</span>
<span class="d2" style="font-size:1.25em">Docker</span>
<span class="d3" style="font-size:1.1em">a bloom filter</span>
<span class="bl" style="font-size:1.6em">a game engine</span>
<span class="d1" style="font-size:1.35em">a key-value store</span>
<span class="d2" style="font-size:1.2em">a Lisp</span>
<span class="am" style="font-size:1.45em">a TCP/IP stack</span>
<span class="d2" style="font-size:1.75em">a web server</span>
<span class="d3" style="font-size:1.1em">a JSON parser</span>
<span class="bl" style="font-size:1.3em">a DNS server</span>
<span class="d1" style="font-size:1.5em">a neural network</span>
<span class="d3" style="font-size:1.2em">Redis</span>
<span class="am" style="font-size:1.35em">a search engine</span>
<span class="d2" style="font-size:1.3em">an emulator</span>
<span class="d3" style="font-size:1.1em">a template engine</span>
<span class="bl" style="font-size:1.4em">a spreadsheet</span>
</div>

<!--
- "Build your own X" is a whole genre — people do it to understand the real thing. Today we pick one: an IaC tool.
- ▶ Just the visual. Gesture across a few, land on the highlighted "an IaC tool" — that's today's pick.
-->

---
routeAlias: I_2
---

# I have a web page. It needs to be on the internet.

<Window title="https://…/files/hello.html" kind="editor">
<div style="background:#f7f7f2;color:#1a1a1a;padding:2.2rem 2.6rem;font-family:Georgia,serif;">
<div style="font-size:1.9rem;font-weight:700;margin-bottom:.6rem;">Deployed by one dumb script</div>
<div style="font-size:1.05rem;color:#444;">KCDC 2026 - Build Your Own IaC</div>
</div>
</Window>

<div class="mt-6 text-xl opacity-90">

We are going to put a web page on the internet using ~~AWS~~ Azure. Then we will build a tool to help us.

</div>

<div class="mt-4 text-base opacity-50">

Goal: learn what Pulumi / Terraform / ARM do.

</div>

<!--
- We want to put an HTML file on the web, using Azure.
- To do that we have to create four objects.
-->

---
routeAlias: I_2b
---

# Everything we're going to make

<div class="mt-6 rounded-lg border-2 border-blue-500 p-4">
  <div class="font-mono text-lg"><b>resource group</b> <span class="opacity-60">· byoiac-demo — the folder it all lives in</span></div>
  <div class="mt-3 rounded-lg border-2 border-blue-400 p-4">
    <div class="font-mono text-lg"><b>storage account</b> <span class="opacity-60">· byoiacdemo2026 — a globally-unique name</span></div>
    <div class="mt-3 rounded-lg border-2 border-blue-300 p-4">
      <div class="font-mono text-lg"><b>container</b> <span class="opacity-60">· files — a public bucket</span></div>
      <div class="mt-3 rounded-lg border-2 border-orange-500 p-4 bg-orange-500/10">
        <div class="font-mono text-lg"><b>hello.html</b> <span class="opacity-60">— the page, with a real URL</span></div>
      </div>
    </div>
  </div>
</div>

<!--
- To do that we have to create four objects.
-->

---
routeAlias: I_3
---

# Start with scripting

<div class="abs-br m-5 flex items-center gap-1.5 text-sm font-semibold px-2.5 py-1 rounded-full" style="background: var(--dg-box2); color: var(--dg-blue-bright); border: 1px solid var(--dg-border);"><span>▶</span> live demo</div>

<Window title="src/1-cli/deploy.sh" kind="editor">

```bash {all}{lines:true}
az group create --name byoiac-demo --location eastus --tags env=demo talk=kcdc

az storage account create --name byoiacdemo2026 --resource-group byoiac-demo \
  --location eastus --sku Standard_LRS --kind StorageV2 --allow-blob-public-access true

az storage container create --name files --account-name byoiacdemo2026 --public-access blob

echo '<h1>Deployed by one dumb script</h1><p>KCDC 2026 - Build Your Own IaC</p>' > hello.html
az storage blob upload --account-name byoiacdemo2026 --container-name files \
  --name hello.html --file hello.html --content-type text/html --overwrite

echo "https://byoiacdemo2026.blob.core.windows.net/files/hello.html"
```

</Window>

<!--
- So we script it, with `az`.
- ⏱ 10 seconds. Do NOT read it aloud. Everyone in the room has written this file.
-->

---
routeAlias: I_4
zoom: 1.0
---

# Let's remove the tool dependency

<Window title="src/2-api/deploy.py" kind="editor">

```py {1-10|12-19|21-29|31-33|35-39|41-49|51-60}{lines:true,maxHeight:'330px'}
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
```

</Window>

<!--
- So we script it, with `az`.
- But can we do it without `az`, to see how it works? Yes: a token and four PUTs.
- ⏱ ~2 min. Then run it.
-->

---
routeAlias: II_1
zoom: 1.0
---

# Run it

<Window title="zsh — byoiac" kind="terminal" maxHeight="335px">

<div v-click="1">

```console
$ python src/2-api/deploy.py
```

</div>
<div v-click="2">

```console
PUT https://management.azure.com/subscriptions/<sub>/resourcegroups/byoiac-demo
  -> 201
PUT .../resourceGroups/byoiac-demo/providers/Microsoft.Storage/storageAccounts/byoiacdemo2026
  -> 202
```

</div>
<div v-click="3">

```console
sleeping 20s for the storage account...
```

</div>
<div v-click="4">

```console
PUT .../storageAccounts/byoiacdemo2026/blobServices/default/containers/files
  -> 201
POST .../storageAccounts/byoiacdemo2026/listServiceSas
  -> 200
PUT https://byoiacdemo2026.blob.core.windows.net/files/hello.html
  -> 201
```

</div>
<div v-click="5">

```console
your page: https://byoiacdemo2026.blob.core.windows.net/files/hello.html
```

</div>

</Window>

<!--
- So run it. The page is live in minute five.
- ▶ RUN IT LIVE. ~26s wall clock, twenty of those are the sleep.
- ▶ Fill the sleep by walking the four PUTs still on the previous slide.
- ▶ THE PAYOFF: browser, not portal. Open `https://byoiacdemo2026.blob.core.windows.net/files/hello.html`. A deployed web page in minute five. Public. Phones welcome.
- ⚠️ Right after a fresh account create the URL can 404 for a few seconds (blob DNS propagation). Narrate the last PUT while it settles.
-->

---
routeAlias: II_1b
---

# Minute five: it's real

<div class="max-w-4xl mx-auto mt-2">
<Window title="portal.azure.com — byoiac-demo" kind="editor">
<img src="./images/portal-rg.png" alt="the resource group in the Azure portal" />
</Window>
<div class="text-center text-sm opacity-70 mt-2">what Azure now holds</div>
</div>

<!--
- So run it. The page is live in minute five.
-->

---
routeAlias: II_2
zoom: 1.0
---

# But it runs every time

<Window title="zsh — byoiac" kind="terminal" maxHeight="335px">

<div v-click="1">

```console
$ python src/2-api/deploy.py
PUT .../resourcegroups/byoiac-demo
  -> 200
PUT .../storageAccounts/byoiacdemo2026
  -> 200
```

</div>
<div v-click="2">

```console
sleeping 20s for the storage account...
```

</div>
<div v-click="3">

```console
PUT .../blobServices/default/containers/files
  -> 200
POST .../listServiceSas
  -> 200
PUT https://byoiacdemo2026.blob.core.windows.net/files/hello.html
  -> 201
```

</div>

</Window>

<div v-click="4" class="mt-4 text-xl">

**Twenty seconds to do nothing.**

</div>

<!--
- So run it. The page is live in minute five.
- But run it again and it re-sends everything and sleeps twenty seconds for nothing.
- ▶ RUN IT AGAIN LIVE. ~23s. Yes, all twenty of those seconds again.
-->

---
routeAlias: II_2a
---

# By the way, we got lucky

<div class="grid grid-cols-2 gap-6 mt-2">

<div>

**Azure: one verb**

```python
# create OR update — same call, same URL
call("PUT", f"{ARM}/.../storageAccounts/{ACCOUNT}",
     {...})
```

<div class="text-lg mt-2 opacity-90">

ARM's PUT is an upsert. Rerunning was safe *by accident*.

</div>

</div>

<div v-click>

**AWS: pick the right verb**

```python
try:
    s3.create_bucket(Bucket=name)   # exists? error
except ClientError:
    pass                            # ...probably fine?
lambda_.create_function(...)        # exists? error
# vs update_function_configuration(...)
```

<div class="text-lg mt-2 opacity-90">

Create-X or Update-X: to pick one, you must first ask **what's out there**.

</div>

</div>

</div>

<!--
- But run it again and it re-sends everything and sleeps twenty seconds for nothing.
- And that only worked because Azure's PUT is an upsert. AWS makes you look before you leap.
- ⏱ ~60s. Cuttable if running long, the story survives without it.
-->

---
routeAlias: II_2b
zoom: 0.92
---

# Failure: Deleting is hard

<Window title="src/2-api/deploy.py" kind="editor">

```diff
- # 3. the container — still ARM, just a deeper URL
- call("PUT", f"{ARM}/subscriptions/{SUB}/resourceGroups/{RG}"
-      f"/providers/Microsoft.Storage/storageAccounts/{ACCOUNT}"
-      f"/blobServices/default/containers/{CONTAINER}?api-version=2023-05-01",
-      {"properties": {"publicAccess": "Blob"}})
-
- print(f"PUT {blob_url}")
- req = urllib.request.Request(f"{blob_url}?{sas}", method="PUT", data=PAGE.encode(),
-     headers={"x-ms-version": "2021-08-06", "x-ms-blob-type": "BlockBlob",
-              "Content-Type": "text/html"})
- with urllib.request.urlopen(req) as resp:
-     print(f"  -> {resp.status}")
```

</Window>

<div v-click class="mt-4 text-xl">

**The file still exists.**

</div>

<div v-click class="mt-3 text-xl">

We need to get rid of it.

</div>

<!--
- And delete a resource from the script and it stays on the internet — a script only says *make this exist*.
- ⏱ ~45 seconds. Don't hedge it, don't hint at the answer.
-->

---
routeAlias: II_2b2
---

# The obvious fix: a line for every delete

<Window title="src/2-api/deploy.py" kind="editor">

```diff
  # ... all the create calls, still up top ...
```

<div v-click="1">

```diff
+ # 2026-08-31 — removed the container + page. keep this forever.
+ call("DELETE", f"{ARM}/.../storageAccounts/{ACCOUNT}"
+      f"/blobServices/default/containers/files?api-version=2023-05-01")
```

</div>
<div v-click="2">

```diff
+ # 2026-09-04 — dropped the old staging account too
+ call("DELETE", f"{ARM}/.../storageAccounts/byoiacdemostaging?api-version=2023-05-01")
```

</div>
<div v-click="3">

```diff
+ # 2026-09-09 — and the temp resource group
+ call("DELETE", f"{ARM}/subscriptions/{SUB}/resourcegroups/byoiac-tmp?api-version=2024-03-01")
```

</div>

</Window>

<div v-click="4" class="mt-4 text-xl">

Removing something = **keeping a delete line forever.**

</div>

<!--
- And delete a resource from the script and it stays on the internet — a script only says *make this exist*.
- So add a DELETE line. Now the script is a log of actions, and nobody can read what the system *is*.
- ⏱ ~60s. Don't say "state" yet. The next slide asks the questions.
-->

---
routeAlias: II_2c
layout: center
class: text-center
---

# How do you do nothing when nothing changed?

# How do you delete?

<!--
- Which leaves two questions: how do you do nothing, and how do you delete?
- ⏱ Let both questions sit. They drive the rest of the hour.
- ▶ FIRE AND FORGET, right now, while this slide is up. The script's stack has to go before Step 3:
  `az group delete -n byoiac-demo --no-wait --yes`
  `--no-wait` returns immediately. Azure finishes in ~60s in the background, which is about how long this slide and the next take.
- ⚠️ If Step 3's first `up` returns 409, the delete is still in flight: wait ten seconds and run it again.
-->

---
routeAlias: II_2d
layout: center
---

# We have a working solution. It's missing one idea.

<div class="text-2xl mt-8 space-y-4">

<div v-click>What's already there? <span class="opacity-60">Then don't redo it.</span></div>

<div v-click>What's no longer wanted? <span class="opacity-60">Then get rid of it.</span></div>

<div v-click>Send <b>only the difference</b>.</div>

</div>

<div v-click class="mt-10 text-2xl">

That's a **diff**. The rest of this talk is making it explicit.

</div>

<!--
- Which leaves two questions: how do you do nothing, and how do you delete?
- Both are one missing idea: it never compares. Send only the difference. That's a **diff**.
-->

---
routeAlias: II_5
zoom: 1.0
---

# The program becomes data

<Window title="infra.yaml" kind="editor">

```yaml {1-5|7-12|14-18|20-25}{lines:true,maxHeight:'290px'}
resources:
  rg:
    type: Microsoft.Resources/resourceGroups
    name: byoiac-demo
    properties: {location: eastus, tags: {env: demo, talk: kcdc}}

  storage:
    type: Microsoft.Storage/storageAccounts
    name: byoiacdemo2026
    resourceGroup: byoiac-demo
    properties: {location: eastus, sku: {name: Standard_LRS},
                 kind: StorageV2, allowBlobPublicAccess: true}

  files:
    type: Microsoft.Storage/…/blobServices/containers
    name: files
    storageAccount: byoiacdemo2026
    properties: {publicAccess: Blob}

  hello:
    type: blob
    name: hello.html
    container: files
    properties: {contentType: text/html,
                 content: "<h1>Deployed by …</h1>"}
```

</Window>

<!--
- Both are one missing idea: it never compares. Send only the difference. That's a **diff**.
- But a diff needs two sides. Side one: the program becomes data.
-->

---
routeAlias: II_3
---

# The matching problem

<svg viewBox="0 0 900 470" class="w-full block" style="max-width:none; margin-top:-0.5rem">
  <!-- PROGRAM -->
  <g>
    <rect x="345" y="32" width="210" height="76" rx="10" class="dgbx" stroke="#3b82f6" stroke-width="2"/>
    <text x="450" y="62" text-anchor="middle" class="dgfg" style="font-size:21px;font-weight:600">Program</text>
    <text x="450" y="88" text-anchor="middle" class="dgmu" style="font-size:14px">what should exist — your names</text>
  </g>

  <!-- CLOUD -->
  <g>
    <rect x="645" y="312" width="210" height="76" rx="10" class="dgam" stroke="#f59e0b" stroke-width="2"/>
    <text x="750" y="342" text-anchor="middle" class="dgfg" style="font-size:21px;font-weight:600">Cloud</text>
    <text x="750" y="368" text-anchor="middle" class="dgmu" style="font-size:14px">what actually exists — its IDs</text>
  </g>

  <!-- 1. the question -->
  <g v-click="1">
    <line x1="500" y1="110" x2="683" y2="310" class="dgln" stroke-width="2.5" stroke-dasharray="7 7"/>
    <rect x="480" y="181" width="236" height="58" rx="8" class="dgbx2 dgbd"/>
    <text x="598" y="205" text-anchor="middle" class="dgfg" style="font-size:15px;font-weight:600">▲ which one is “files”?</text>
    <text x="598" y="227" text-anchor="middle" class="dgmu" style="font-size:13px;font-style:italic">the cloud doesn't keep your mapping</text>
  </g>

  <!-- 2. state as the recorded mapping -->
  <g v-click="2">
    <rect x="45" y="312" width="210" height="76" rx="10" class="dgbx" stroke="#3b82f6" stroke-width="2"/>
    <text x="150" y="342" text-anchor="middle" class="dgfg" style="font-size:21px;font-weight:600">State</text>
    <text x="150" y="368" text-anchor="middle" class="dgmu" style="font-size:14px">your name → the ID it gave back</text>
    <line x1="400" y1="110" x2="217" y2="310" stroke="#3b82f6" stroke-width="2.5"/>
    <rect x="201" y="181" width="212" height="58" rx="8" class="dgbx2 dgbd"/>
    <text x="307" y="205" text-anchor="middle" class="dgbb" style="font-size:15px;font-weight:600">■ you changed the code</text>
    <text x="307" y="227" text-anchor="middle" class="dgmu" style="font-size:13px">expected</text>
  </g>

  <!-- 3. drift -->
  <g v-click="3">
    <line x1="257" y1="350" x2="643" y2="350" stroke="#f59e0b" stroke-width="2.5"/>
    <rect x="344" y="321" width="212" height="58" rx="8" class="dgbx2 dgbd"/>
    <text x="450" y="345" text-anchor="middle" class="dgab" style="font-size:15px;font-weight:600">▲ someone else did</text>
    <text x="450" y="367" text-anchor="middle" class="dgmu" style="font-size:13px">unexpected</text>
  </g>

  <!-- 4. punchline -->
  <g v-click="4">
    <text x="450" y="440" text-anchor="middle" class="dgfg" style="font-size:17px">The diff is only computable on top of this mapping.</text>
    <text x="450" y="464" text-anchor="middle" class="dgmu" style="font-size:15px">State is memory of what you made, written down at create time.</text>
  </g>
</svg>

<!--
- But a diff needs two sides. Side one: the program becomes data.
- Side two is the cloud, and nothing maps your names to its IDs — so write it down at creation. That's **state**.
- ▶ Base: Program + Cloud only. Let them sit for a moment. The diff we just promised has to run between these two lists.
- ⏱ ~90 seconds. Don't explain drift yet. Just name the edge, we come back to it.
-->

---
routeAlias: II_4c
---

# The same picture, live

<IaCSandbox :stage="1" />

<!--
- Here's that triangle running.
- ▶ LIVE. This toy is the DESTINATION, the loop working, and the next step of code builds it, memory first, then the loop. Program already says `rg` and `storage`. Hit `up`: `+ rg  + storage`, rows land in Cloud, then State.
- ▶ Hit `up` AGAIN → `= rg  = storage — nothing sent`. Point at it.
- ▶ Now DELETE the `storage` lines from Program. `up` → `- storage  = rg`. The row disappears from Cloud and from State.
- ▶ (optional) Edit `rg`'s tag → `~ rg`. Create, update, delete, skip: the whole vocabulary, one button. All of it gets built in the next step.
- ⏱ 90 sec. Fallback if a live demo dies later: this needs no cloud and no wifi.
-->

---
routeAlias: II_4
---

# Step 3 — first, the memory

<Window title="src/3-state/engine.py" kind="editor">

```py {1-8|10-15}{lines:true}
STATE_FILE = "state.json"

# ---- pillar 1: state — what we THINK exists --------------------------------

def load_state():
    return json.load(open(STATE_FILE)) if os.path.exists(STATE_FILE) else {}

def save_state(state):
    json.dump(state, open(STATE_FILE, "w"), indent=2)

# ...and after every resource the loop touches, further down the file:

        call("PUT", url_for(res), res["properties"])
        state[key] = {"res": res, "saved": res["properties"]}
        save_state(state)
```

</Window>

<div v-click class="mt-4 text-xl">

The whole answer to "what's mine?" is **a JSON file the tool writes as it works.**

</div>

<!--
- Here's that triangle running.
- So build it. The memory is two functions.
-->

---
routeAlias: II_6
zoom: 1.0
---

# Step 3 — reconcile: compare, then act

<Window title="src/3-state/engine.py" kind="editor">

```py {1-6|8-19|9-13|14-19|13,19}{lines:true,maxHeight:'310px'}
def diff(desired, state):
    creates = [k for k in desired if k not in state]
    deletes = [k for k in state if k not in desired]
    updates = [k for k in desired if k in state
               and desired[k]["properties"] != state[k]["saved"]]
    return creates, updates, deletes

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
```

</Window>

<!--
- The loop is three set operations.
-->

---
routeAlias: II_6b
zoom: 1.0
---

# Step 3 — the vocabulary

<Window title="src/3-state/engine.py" kind="editor">

```py {1-3|4-10}{lines:true}
def url_for(res):
    if res["type"] == "Microsoft.Resources/resourceGroups":
        return f"{BASE}/subscriptions/{SUB}/resourcegroups/{res['name']}?api-version=2024-03-01"
    if res["type"] == "Microsoft.Storage/storageAccounts/blobServices/containers":
        return (f"{BASE}/subscriptions/{SUB}/resourceGroups/{res['resourceGroup']}"
                f"/providers/Microsoft.Storage/storageAccounts/{res['storageAccount']}"
                f"/blobServices/default/containers/{res['name']}?api-version=2023-05-01")
    return (f"{BASE}/subscriptions/{SUB}/resourceGroups/{res['resourceGroup']}"
            f"/providers/{res['type']}/{res['name']}?api-version=2023-05-01")
```

</Window>

<div v-click class="mt-4 text-xl">

This is the only type-specific code in the tool.

</div>

<!--
- The loop is three set operations.
- And one function holds every URL shape.
-->

---
routeAlias: II_9
zoom: 1.0
---

# Step 3 — run it

<Window title="zsh — byoiac" kind="terminal" maxHeight="335px">

<div v-click="1">

```console
$ python src/3-state/engine.py up      # initial up
  + create rg
  + create storage
  + create files
  + create hello
  + rg
  + storage
  + files
  + hello
```

</div>
<div v-click="2">

```console
$ python src/3-state/engine.py up      # running again
  no changes.
```

</div>
<div v-click="3">

```console
$ cat state.json      # looking at the state file
{ "rg":      { "res": { ... }, "saved": { "location": "eastus", "tags": { ... } } },
  "storage": { "res": { ... }, "saved": { ... } },
  "files":   { "res": { ... }, "saved": { ... } },
  "hello":   { "res": { ... }, "saved": { "contentType": "text/html", ... } } }
```

</div>
<div v-click="4">

```console
$ vim infra.yaml      # edit talk: kcdc -> talk: kcdc2026
$ python src/3-state/engine.py plan
  ~ update rg
$ python src/3-state/engine.py up
  ~ update rg
  ~ rg
```

</div>

</Window>

<div v-click="5" class="mt-3 text-lg">

Run two sent **nothing**. `plan` called **zero** write APIs, and `state.json` is a **belief**, not a fact: nothing was checked.

</div>

<!--
- Run it: nothing changed, nothing sent. And state is a **belief** — nothing was checked.
- ▶ RUN IT LIVE, in order. First `up`: the whole stack, the same four things the script made. **~26s measured** (2026-09-01): the gap after `+ storage` is the script's `sleep(20)` shrug, inherited verbatim. Narrate it: "twenty seconds of guessing. We fix that next."
- ⚠️ 409 on the first `up` = the earlier `az group delete` is still in flight. Wait ten seconds and run it again.
- ▶ (click 4) Edit `talk: kcdc → kcdc2026` live, `plan`: one line, zero write APIs. Then `up`: same line, and now it's true. Plan and apply are the same subtraction. Only one of them phones the cloud.
- ▶ PORTAL: Tags blade shows `kcdc2026`. Revert + `up` again while talking.
- ⚠️ All four transcripts are REAL captures (2026-09-01, one sitting, live against Azure): up 26.4s / instant no-changes / state shape verified / tag cycle `~ update rg` → `~ rg` confirmed in the portal-side tags. Tag lives in an inline dict (`tags: {env: demo, talk: kcdc}`). Edit in the editor, not with sed.
-->

---
routeAlias: II_10
title: 114 lines
---

# 114 lines. It works.

<div class="grid grid-cols-2 gap-10 items-center mt-2">

<div>
<Window title="byoiacdemo2026.blob.core.windows.net/files/hello.html" kind="editor">
<img src="./images/live-page.png" alt="the deployed page, live" />
</Window>
<div class="text-center text-sm opacity-60 mt-2">live on the internet — deployed by our tool</div>
</div>

<div class="text-center">

<div class="font-mono text-base opacity-60">$ python src/3-state/engine.py up</div>

<div class="text-[8rem] leading-none font-bold mt-3">114</div>
<div class="text-2xl">lines of Python</div>

<div v-click class="mt-10 text-2xl">

State · diff · reconcile.
**A working IaC tool.**

</div>

</div>

</div>

<!--
- In 114 lines the page is back — and now it's a tool that knows what it made.
- ▶ THE PAYOFF: browser, not portal. Open the URL. Public, phones welcome.
- ⚠️ Right after a fresh account create the URL can 404 for a few seconds (blob DNS propagation). Narrate while it settles. Verified 200 within ~2s on a warm account (2026-08-31).
- ⏱ PAUSE. Top of the first arc, let them enjoy it. "State, diff, reconcile — and now you know how all of them work."
-->

---
routeAlias: II_10b
---

# Now it plans deletes and reruns

<IaCSandbox :stage="3" />

<!--
- Demo: now our tool can handle deletes and no-ops — the two questions, answered.
- ▶ LIVE. Change a row's tag in Program → `plan` → `~ update`. Nothing moved: Cloud and State are untouched.
- ▶ Delete a whole row out of Program → `plan` → `- delete`. Still nothing moved.
- ▶ `up` → it's really gone. Out of Cloud, out of State.
- ⏱ ~60 sec. Also a wifi fallback: no cloud needed.
-->

---
routeAlias: II_10b3
---

# Problem: Someone tidies a file

````md magic-move
```yaml
resources:
  rg:                 # the group
    type: Microsoft.Resources/resourceGroups
    ...
  storage:            # the account
    type: Microsoft.Storage/storageAccounts
    ...
  files:              # the container
    type: .../blobServices/containers
    ...
  hello:              # the page — the whole point
    type: blob
    ...
```
```yaml
resources:
  hello:              # the page — the whole point
    type: blob
    ...
  rg:                 # the group
    type: Microsoft.Resources/resourceGroups
    ...
  storage:            # the account
    type: Microsoft.Storage/storageAccounts
    ...
  files:              # the container
    type: .../blobServices/containers
    ...
```
````

<div class="mt-3 text-sm opacity-60 font-mono">src/3-state/infra-tidied.yaml</div>

<!--
- Demo: now our tool can handle deletes and no-ops — the two questions, answered.
- But someone tidies the file and moves the page to the top.
- ▶ CLICK, the block slides up. Say nothing while it moves.
-->

---
routeAlias: II_10c
zoom: 1.0
---

# Run it

<Window title="zsh — byoiac" kind="terminal" maxHeight="335px">

<div v-click="1">

```console
$ python src/3-state/engine.py destroy      # clean slate first
  - delete rg
  - delete storage
  - delete files
  - delete hello
  - hello
  - files
  - storage
  - rg
```

</div>
<div v-click="2">

```console
$ cp src/3-state/infra-tidied.yaml src/3-state/infra.yaml      # the tidied file
$ python src/3-state/engine.py up      # same stack, page moved to the top
  + create hello
  + create rg
  + create storage
  + create files
```

</div>
<div v-click="3">

```console
  + hello
Traceback (most recent call last):
  ...
  File "src/3-state/engine.py", line 62, in blob_sas
    return out["serviceSasToken"]
TypeError: 'NoneType' object is not subscriptable
```

</div>

</Window>

<div v-click="4" class="mt-4 text-xl">

The tool created things in **file order**, and that won't scale.

</div>

<!--
- Run it and it crashes: it created things in file order.
- ⚠️ Both transcripts are REAL captures (2026-09-01, live against Azure). Note the destroy's apply lines run BACKWARDS (`- hello … - rg`): the engine tears down with `reversed(deletes)`. File-order deletes crashed for real (rg cascade killed the account before the blob delete could sign its SAS), so "teardown = setup order, backwards" is IN the engine. More borrowed luck. `II_12`'s reversed(ordered()) is what it grows into. Crash line 62 confirmed. The `up` from empty state creates nothing, so no cleanup needed. Repro: `cp src/3-state/infra-tidied.yaml src/3-state/infra.yaml && python src/3-state/engine.py up`. Restore with `git checkout src/3-state/infra.yaml`.
-->

---
routeAlias: II_10d
---

# A Go program couldn't have shipped this

<div class="grid grid-cols-2 gap-6 mt-4">

<div>

**Python** — dicts remember insertion order. Guaranteed, since 3.7.

```python
for key in resources:   # file order
    create(key)         # works. every run.
```

<div class="font-mono text-sm mt-2 opacity-80">

```console
$ python deploy.py    # run 1, 2, 3...
+ rg  + storage  + files  + hello   # always this order
```

</div>

</div>

<div v-click>

**Go** — map order is randomized. *On purpose.*

```go
for name := range resources {  // shuffled
    create(name)               // every run
}
```

<div class="font-mono text-sm mt-2 opacity-80">

```console
$ go run deploy.go    # run 1
+ hello   ✗ storage does not exist
$ go run deploy.go    # run 2 — different order, different crash
```

</div>

</div>

</div>

<!--
- Run it and it crashes: it created things in file order.
- And Python hid the bug. Go would have failed the first afternoon.
- ⏱ ~45s. Pure fun + one real point. Cuttable if long, second in the trim order after II_2a.
-->

---
routeAlias: II_10e
---

# The whole problem, four names

<svg viewBox="0 0 900 210" class="w-full block" style="max-width:none; margin-top:1rem">
  <defs>
    <marker id="arr" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
      <path d="M0,0 L8,4 L0,8 z" class="dglnf"/>
    </marker>
  </defs>
  <g>
    <rect x="40"  y="60" width="150" height="60" rx="9" class="dgbx" stroke="#3b82f6" stroke-width="2"/>
    <text x="115" y="97" text-anchor="middle" class="dgfg" style="font-size:20px;font-weight:600">rg</text>
    <rect x="270" y="60" width="150" height="60" rx="9" class="dgbx" stroke="#3b82f6" stroke-width="2"/>
    <text x="345" y="97" text-anchor="middle" class="dgfg" style="font-size:20px;font-weight:600">storage</text>
    <rect x="500" y="60" width="150" height="60" rx="9" class="dgbx" stroke="#3b82f6" stroke-width="2"/>
    <text x="575" y="97" text-anchor="middle" class="dgfg" style="font-size:20px;font-weight:600">files</text>
    <rect x="730" y="60" width="150" height="60" rx="9" class="dgbx" stroke="#3b82f6" stroke-width="2"/>
    <text x="805" y="97" text-anchor="middle" class="dgfg" style="font-size:20px;font-weight:600">hello</text>
    <line x1="270" y1="90" x2="196" y2="90" class="dgln" stroke-width="2.5" marker-end="url(#arr)"/>
    <line x1="500" y1="90" x2="426" y2="90" class="dgln" stroke-width="2.5" marker-end="url(#arr)"/>
    <line x1="730" y1="90" x2="656" y2="90" class="dgln" stroke-width="2.5" marker-end="url(#arr)"/>
    <text x="450" y="35" text-anchor="middle" class="dgmu" style="font-size:15px;font-style:italic">→ means "needs"</text>
  </g>
</svg>

<div class="mt-2 text-xl space-y-3">

<div v-click><span class="font-mono text-2xl">✗</span> <code>hello · rg · storage · files</code> <span class="opacity-60">— hello's parents don't exist yet. Crash.</span></div>

<div v-click><span class="font-mono text-2xl">✓</span> <code>rg · storage · files · hello</code> <span class="opacity-60">— every arrow satisfied.</span></div>

</div>

<!--
- The truth was never the order, it was the arrows. Store arrows, derive order.
- ⏱ ~45s.
-->

---
routeAlias: II_11
zoom: 0.9
---

# Step 4 — write down dependencies

<Window title="src/3-state → src/4-graph — infra.yaml" kind="editor">

````md magic-move {lines:true}

```yaml
resources:
  rg:
    name: byoiac-demo
    ...
  storage:
    name: byoiacdemo2026
    resourceGroup: byoiac-demo
    ...
  files:
    name: files
    storageAccount: byoiacdemo2026
    ...
  hello:
    name: hello.html
    container: files
    ...
```

```yaml
resources:
  rg:
    name: byoiac-demo
    ...
  storage:
    name: byoiacdemo2026
    resourceGroup: byoiac-demo
    dependsOn: [rg]             # Pulumi infers this from ${rg.name} — we can't
    ...
  files:
    name: files
    storageAccount: byoiacdemo2026
    dependsOn: [storage]
    ...
  hello:
    name: hello.html
    container: files
    dependsOn: [files]
    ...
```

````

</Window>

<!--
- So write them down: `dependsOn`. It's what the script already had.
-->

---
routeAlias: II_11c
clicks: 12
---

# Arrows in, order out

<svg viewBox="0 0 900 140" class="w-full block" style="max-width:none">
  <defs>
    <marker id="warr" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
      <path d="M0,0 L8,4 L0,8 z" class="dglnf"/>
    </marker>
  </defs>

  <rect x="40"  y="50"  width="150" height="40" rx="9" class="dgbx dgbd" stroke-width="1.5"/>
  <rect x="270" y="50"  width="150" height="40" rx="9" class="dgbx dgbd" stroke-width="1.5"/>
  <rect x="500" y="6"   width="150" height="40" rx="9" class="dgbx dgbd" stroke-width="1.5"/>
  <rect x="730" y="6"   width="150" height="40" rx="9" class="dgbx dgbd" stroke-width="1.5"/>
  <rect x="500" y="94"  width="150" height="40" rx="9" class="dgbx dgbd" stroke-width="1.5"/>

  <rect v-motion :initial="{opacity:0}" :click-5="{opacity:1}"  x="40"  y="50"  width="150" height="40" rx="9" class="dgam" stroke="#f59e0b" stroke-width="2.5"/>
  <rect v-motion :initial="{opacity:0}" :click-6="{opacity:1}"  x="270" y="50"  width="150" height="40" rx="9" class="dgam" stroke="#f59e0b" stroke-width="2.5"/>
  <rect v-motion :initial="{opacity:0}" :click-7="{opacity:1}"  x="500" y="6"   width="150" height="40" rx="9" class="dgam" stroke="#f59e0b" stroke-width="2.5"/>
  <rect v-motion :initial="{opacity:0}" :click-8="{opacity:1}"  x="730" y="6"   width="150" height="40" rx="9" class="dgam" stroke="#f59e0b" stroke-width="2.5"/>
  <rect v-motion :initial="{opacity:0}" :click-11="{opacity:1}" x="500" y="94"  width="150" height="40" rx="9" class="dgam" stroke="#f59e0b" stroke-width="2.5"/>

  <line x1="266" y1="70"  x2="196" y2="70" class="dgln" stroke-width="2.5" marker-end="url(#warr)"/>
  <line x1="496" y1="26"  x2="426" y2="56" class="dgln" stroke-width="2.5" marker-end="url(#warr)"/>
  <line x1="726" y1="26"  x2="656" y2="26" class="dgln" stroke-width="2.5" marker-end="url(#warr)"/>
  <line x1="496" y1="114" x2="426" y2="84" class="dgln" stroke-width="2.5" marker-end="url(#warr)"/>

  <rect v-motion :initial="{opacity:0}" :click-4="{opacity:1}"  x="40"  y="50"  width="150" height="40" rx="9" fill="none" stroke="#3b82f6" stroke-width="3.5"/>
  <rect v-motion :initial="{opacity:0}" :click-3="{opacity:1}"  x="270" y="50"  width="150" height="40" rx="9" fill="none" stroke="#3b82f6" stroke-width="3.5"/>
  <rect v-motion :initial="{opacity:0}" :click-2="{opacity:1}"  x="500" y="6"   width="150" height="40" rx="9" fill="none" stroke="#3b82f6" stroke-width="3.5"/>
  <rect v-motion :initial="{opacity:0}" :click-1="{opacity:1}"  x="730" y="6"   width="150" height="40" rx="9" fill="none" stroke="#3b82f6" stroke-width="3.5"/>
  <rect v-motion :initial="{opacity:0}" :click-9="{opacity:1}"  x="500" y="94"  width="150" height="40" rx="9" fill="none" stroke="#3b82f6" stroke-width="3.5"/>

  <text v-motion :initial="{opacity:0}" :click-10="{opacity:1}" x="345" y="40" text-anchor="middle" class="dgbb" style="font-size:13px;font-style:italic">already visited — skip</text>

  <text x="115" y="76"  text-anchor="middle" class="dgfg" style="font-size:18px;font-weight:600">rg</text>
  <text x="345" y="76"  text-anchor="middle" class="dgfg" style="font-size:18px;font-weight:600">storage</text>
  <text x="575" y="32"  text-anchor="middle" class="dgfg" style="font-size:18px;font-weight:600">files</text>
  <text x="805" y="32"  text-anchor="middle" class="dgfg" style="font-size:18px;font-weight:600">hello</text>
  <text x="575" y="120" text-anchor="middle" class="dgfg" style="font-size:18px;font-weight:600">cdn</text>
</svg>

<div class="grid grid-cols-[1.5fr_1fr] gap-10 mt-1">

<div>
<div class="text-xs opacity-55 mb-2">the walk <span class="opacity-70">— nothing is written down on the way in</span></div>
<div class="font-mono text-sm space-y-1">
<div v-motion :initial="{opacity:0,x:-26}" :click-1="{opacity:1,x:0}">visit(<b>hello</b>)<span class="opacity-50"> — needs files</span></div>
<div class="pl-4" v-motion :initial="{opacity:0,x:-26}" :click-2="{opacity:1,x:0}">visit(<b>files</b>)<span class="opacity-50"> — needs storage</span></div>
<div class="pl-8" v-motion :initial="{opacity:0,x:-26}" :click-3="{opacity:1,x:0}">visit(<b>storage</b>)<span class="opacity-50"> — needs rg</span></div>
<div class="pl-12" v-motion :initial="{opacity:0,x:-26}" :click-4="{opacity:1,x:0}">visit(<b>rg</b>)<span class="opacity-50"> — no arrows</span></div>
<div class="h-3"></div>
<div v-motion :initial="{opacity:0,x:-26}" :click-9="{opacity:1,x:0}">visit(<b>cdn</b>)<span class="opacity-50"> — needs storage too</span></div>
<div class="pl-4 dgbb-t" v-motion :initial="{opacity:0,x:-26}" :click-10="{opacity:1,x:0}">visit(<b>storage</b>) → <b>in done, return</b></div>
</div>
</div>

<div>
<div class="text-xs opacity-55 mb-2">order <span class="opacity-70">— written on the way back out</span></div>
<div class="font-mono text-sm space-y-1">
<div class="dgab-t" v-motion :initial="{opacity:0,x:-300}" :click-5="{opacity:1,x:0}"><b>rg</b></div>
<div class="dgab-t" v-motion :initial="{opacity:0,x:-300}" :click-6="{opacity:1,x:0}"><b>storage</b></div>
<div class="dgab-t" v-motion :initial="{opacity:0,x:-300}" :click-7="{opacity:1,x:0}"><b>files</b></div>
<div class="dgab-t" v-motion :initial="{opacity:0,x:-300}" :click-8="{opacity:1,x:0}"><b>hello</b></div>
<div class="dgab-t" v-motion :initial="{opacity:0,x:-300}" :click-11="{opacity:1,x:0}"><b>cdn</b></div>
</div>
</div>

</div>

<div v-motion :initial="{opacity:0,y:12}" :click-12="{opacity:1,y:0}" class="mt-2 text-lg">

A name is written down only once everything it points at already is. <b>That's the whole sort.</b>

</div>

<!--
- Here's the walk: nothing is written down on the way in, names are written on the way back out.
-->

---
routeAlias: II_12
---

# Step 4 — walking the graph

<Window title="src/4-graph/engine.py" kind="editor">

```py {1-11|3-9|13-18|16}{lines:true}
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

def wait_ready(res):  # 201/202 = "working on it" — poll until the cloud is done
    while True:
        code, actual = call("GET", url_for(res))
        if code != 404 and (actual or {}).get("properties", {}).get(
                "provisioningState") == "Succeeded":
            return
        time.sleep(2)
```

</Window>

<!--
- And that's eleven lines of code — plus `wait_ready`, what `sleep(20)` grew up into.
- ⏱ THIS is the dead-air filler slide. Come back here during the next slide's ~20s wait.
-->

---
routeAlias: II_12b
clicks: 5
---

# Counters in, waves out

<svg viewBox="0 0 900 148" class="w-full block" style="max-width:none">
  <defs>
    <marker id="karr" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
      <path d="M0,0 L8,4 L0,8 z" class="dglnf"/>
    </marker>
  </defs>

  <rect x="40"  y="50" width="150" height="40" rx="9" class="dgbx dgbd" stroke-width="1.5"/>
  <rect x="270" y="50" width="150" height="40" rx="9" class="dgbx dgbd" stroke-width="1.5"/>
  <rect x="500" y="6"  width="150" height="40" rx="9" class="dgbx dgbd" stroke-width="1.5"/>
  <rect x="730" y="6"  width="150" height="40" rx="9" class="dgbx dgbd" stroke-width="1.5"/>
  <rect x="500" y="94" width="150" height="40" rx="9" class="dgbx dgbd" stroke-width="1.5"/>

  <rect v-motion :initial="{opacity:0}" :click-2="{opacity:1}" x="40"  y="50" width="150" height="40" rx="9" class="dgam" stroke="#f59e0b" stroke-width="2.5"/>
  <rect v-motion :initial="{opacity:0}" :click-3="{opacity:1}" x="270" y="50" width="150" height="40" rx="9" class="dgam" stroke="#f59e0b" stroke-width="2.5"/>
  <rect v-motion :initial="{opacity:0}" :click-4="{opacity:1}" x="500" y="6"  width="150" height="40" rx="9" class="dgam" stroke="#f59e0b" stroke-width="2.5"/>
  <rect v-motion :initial="{opacity:0}" :click-5="{opacity:1}" x="730" y="6"  width="150" height="40" rx="9" class="dgam" stroke="#f59e0b" stroke-width="2.5"/>
  <rect v-motion :initial="{opacity:0}" :click-4="{opacity:1}" x="500" y="94" width="150" height="40" rx="9" class="dgam" stroke="#f59e0b" stroke-width="2.5"/>

  <line x1="266" y1="70"  x2="196" y2="70" class="dgln" stroke-width="2.5" marker-end="url(#karr)"/>
  <line x1="496" y1="26"  x2="426" y2="56" class="dgln" stroke-width="2.5" marker-end="url(#karr)"/>
  <line x1="726" y1="26"  x2="656" y2="26" class="dgln" stroke-width="2.5" marker-end="url(#karr)"/>
  <line x1="496" y1="114" x2="426" y2="84" class="dgln" stroke-width="2.5" marker-end="url(#karr)"/>

  <rect v-motion :initial="{opacity:0}" :click-1="{opacity:1}" :click-2="{opacity:0}" x="40"  y="50" width="150" height="40" rx="9" fill="none" stroke="#3b82f6" stroke-width="3.5"/>
  <rect v-motion :initial="{opacity:0}" :click-2="{opacity:1}" :click-3="{opacity:0}" x="270" y="50" width="150" height="40" rx="9" fill="none" stroke="#3b82f6" stroke-width="3.5"/>
  <rect v-motion :initial="{opacity:0}" :click-3="{opacity:1}" :click-4="{opacity:0}" x="500" y="6"  width="150" height="40" rx="9" fill="none" stroke="#3b82f6" stroke-width="3.5"/>
  <rect v-motion :initial="{opacity:0}" :click-3="{opacity:1}" :click-4="{opacity:0}" x="500" y="94" width="150" height="40" rx="9" fill="none" stroke="#3b82f6" stroke-width="3.5"/>
  <rect v-motion :initial="{opacity:0}" :click-4="{opacity:1}" :click-5="{opacity:0}" x="730" y="6"  width="150" height="40" rx="9" fill="none" stroke="#3b82f6" stroke-width="3.5"/>

  <g v-motion :initial="{opacity:0}" :click-1="{opacity:1}">
    <circle cx="180" cy="58"  r="12" class="dgbx2 dgbd" stroke-width="1.5"/>
    <circle cx="410" cy="58"  r="12" class="dgbx2 dgbd" stroke-width="1.5"/>
    <circle cx="640" cy="14"  r="12" class="dgbx2 dgbd" stroke-width="1.5"/>
    <circle cx="870" cy="14"  r="12" class="dgbx2 dgbd" stroke-width="1.5"/>
    <circle cx="640" cy="102" r="12" class="dgbx2 dgbd" stroke-width="1.5"/>
  </g>

  <text v-motion :initial="{opacity:0}" :click-1="{opacity:1}" x="180" cy="0" y="63" text-anchor="middle" class="dgbb" style="font-size:14px;font-weight:700">0</text>

  <text v-motion :initial="{opacity:0}" :click-1="{opacity:1}" :click-2="{opacity:0}" x="410" y="63" text-anchor="middle" class="dgmu" style="font-size:14px;font-weight:700">1</text>
  <text v-motion :initial="{opacity:0}" :click-2="{opacity:1}" x="410" y="63" text-anchor="middle" class="dgbb" style="font-size:14px;font-weight:700">0</text>

  <text v-motion :initial="{opacity:0}" :click-1="{opacity:1}" :click-3="{opacity:0}" x="640" y="19" text-anchor="middle" class="dgmu" style="font-size:14px;font-weight:700">1</text>
  <text v-motion :initial="{opacity:0}" :click-3="{opacity:1}" x="640" y="19" text-anchor="middle" class="dgbb" style="font-size:14px;font-weight:700">0</text>

  <text v-motion :initial="{opacity:0}" :click-1="{opacity:1}" :click-3="{opacity:0}" x="640" y="107" text-anchor="middle" class="dgmu" style="font-size:14px;font-weight:700">1</text>
  <text v-motion :initial="{opacity:0}" :click-3="{opacity:1}" x="640" y="107" text-anchor="middle" class="dgbb" style="font-size:14px;font-weight:700">0</text>

  <text v-motion :initial="{opacity:0}" :click-1="{opacity:1}" :click-4="{opacity:0}" x="870" y="19" text-anchor="middle" class="dgmu" style="font-size:14px;font-weight:700">1</text>
  <text v-motion :initial="{opacity:0}" :click-4="{opacity:1}" x="870" y="19" text-anchor="middle" class="dgbb" style="font-size:14px;font-weight:700">0</text>

  <text x="115" y="76"  text-anchor="middle" class="dgfg" style="font-size:18px;font-weight:600">rg</text>
  <text x="345" y="76"  text-anchor="middle" class="dgfg" style="font-size:18px;font-weight:600">storage</text>
  <text x="575" y="32"  text-anchor="middle" class="dgfg" style="font-size:18px;font-weight:600">files</text>
  <text x="805" y="32"  text-anchor="middle" class="dgfg" style="font-size:18px;font-weight:600">hello</text>
  <text x="575" y="120" text-anchor="middle" class="dgfg" style="font-size:18px;font-weight:600">cdn</text>
</svg>

<div class="grid grid-cols-[1fr_1fr] gap-10 mt-1">

<div>
<div class="text-xs opacity-55 mb-2" v-motion :initial="{opacity:0}" :click-1="{opacity:0.55}">the badge = arrows still unmet · <span class="dgbb-t font-bold">0</span> = ready</div>
<div class="font-mono text-sm space-y-1">
<div v-motion :initial="{opacity:0,x:-26}" :click-2="{opacity:1,x:0}">take <b>rg</b> <span class="opacity-50">→ storage 1→0</span></div>
<div v-motion :initial="{opacity:0,x:-26}" :click-3="{opacity:1,x:0}">take <b>storage</b> <span class="opacity-50">→ files 1→0, cdn 1→0</span></div>
<div v-motion :initial="{opacity:0,x:-26}" :click-4="{opacity:1,x:0}">take <b>files</b>, <b>cdn</b> <span class="opacity-50">→ hello 1→0</span></div>
<div v-motion :initial="{opacity:0,x:-26}" :click-5="{opacity:1,x:0}">take <b>hello</b> <span class="opacity-50">→ nothing left</span></div>
</div>
</div>

<div>
<div class="text-xs opacity-55 mb-2">waves</div>
<div class="font-mono text-sm space-y-1">
<div v-motion :initial="{opacity:0,x:-260}" :click-2="{opacity:1,x:0}"><span class="opacity-40 mr-3">1</span><span class="dgab-t font-bold">rg</span></div>
<div v-motion :initial="{opacity:0,x:-260}" :click-3="{opacity:1,x:0}"><span class="opacity-40 mr-3">2</span><span class="dgab-t font-bold">storage</span></div>
<div v-motion :initial="{opacity:0,x:-260}" :click-4="{opacity:1,x:0}"><span class="opacity-40 mr-3">3</span><span class="dgab-t font-bold">files</span><span class="opacity-40 mx-2">+</span><span class="dgab-t font-bold">cdn</span></div>
<div v-motion :initial="{opacity:0,x:-260}" :click-5="{opacity:1,x:0}"><span class="opacity-40 mr-3">4</span><span class="dgab-t font-bold">hello</span></div>
</div>
</div>

</div>

<!--
- (bonus) Counters instead of a call stack — everything at zero goes at once. That's the go-fast plan every real engine runs.
-->

---
routeAlias: II_12c
clicks: 6
zoom: 0.92
---

# The loop, and its three variables

<div class="grid grid-cols-[1.15fr_1fr] gap-8 mt-2">

<div>

```py {1-2|4-5|7-15|7-15|7-15|7-15}{lines:true}
unmet = {k: len(r["dependsOn"]) for k, r in res.items()}
waiting_on = invert(res)          # rg -> [storage], storage -> [files, cdn]

ready = [k for k in unmet if unmet[k] == 0]
out = []

while ready:
    out.append(ready)             # one wave — these go at once
    nxt = []
    for k in ready:
        for d in waiting_on[k]:
            unmet[d] -= 1         # one arrow met
            if unmet[d] == 0:
                nxt.append(d)     # last arrow met — it's ready
    ready = nxt
```

</div>

<div class="font-mono text-sm">

<div class="text-xs opacity-55 mb-1">unmet <span class="opacity-70">— arrows still owed</span></div>
<div class="space-y-0.5">
  <div><span class="inline-block w-20 opacity-70">rg</span><span class="dgbb-t font-bold">0</span></div>
  <div><span class="inline-block w-20 opacity-70">storage</span><span class="inline-grid align-baseline"><span class="col-start-1 row-start-1" v-motion :initial="{opacity:1}" :click-3="{opacity:0}">1</span><span class="col-start-1 row-start-1 dgbb-t font-bold" v-motion :initial="{opacity:0}" :click-3="{opacity:1}">0</span></span></div>
  <div><span class="inline-block w-20 opacity-70">files</span><span class="inline-grid align-baseline"><span class="col-start-1 row-start-1" v-motion :initial="{opacity:1}" :click-4="{opacity:0}">1</span><span class="col-start-1 row-start-1 dgbb-t font-bold" v-motion :initial="{opacity:0}" :click-4="{opacity:1}">0</span></span></div>
  <div><span class="inline-block w-20 opacity-70">cdn</span><span class="inline-grid align-baseline"><span class="col-start-1 row-start-1" v-motion :initial="{opacity:1}" :click-4="{opacity:0}">1</span><span class="col-start-1 row-start-1 dgbb-t font-bold" v-motion :initial="{opacity:0}" :click-4="{opacity:1}">0</span></span></div>
  <div><span class="inline-block w-20 opacity-70">hello</span><span class="inline-grid align-baseline"><span class="col-start-1 row-start-1" v-motion :initial="{opacity:1}" :click-5="{opacity:0}">1</span><span class="col-start-1 row-start-1 dgbb-t font-bold" v-motion :initial="{opacity:0}" :click-5="{opacity:1}">0</span></span></div>
</div>

<div class="text-xs opacity-55 mt-5 mb-1">ready <span class="opacity-70">— everything at zero</span></div>
<div class="relative h-6">
  <div class="absolute opacity-40" v-motion :initial="{opacity:0.4}" :click-2="{opacity:0}">[]</div>
  <div class="absolute dgbb-t font-bold" v-motion :initial="{opacity:0}" :click-2="{opacity:1}" :click-3="{opacity:0}">[rg]</div>
  <div class="absolute dgbb-t font-bold" v-motion :initial="{opacity:0}" :click-3="{opacity:1}" :click-4="{opacity:0}">[storage]</div>
  <div class="absolute dgbb-t font-bold" v-motion :initial="{opacity:0}" :click-4="{opacity:1}" :click-5="{opacity:0}">[files, cdn]</div>
  <div class="absolute dgbb-t font-bold" v-motion :initial="{opacity:0}" :click-5="{opacity:1}" :click-6="{opacity:0}">[hello]</div>
  <div class="absolute opacity-40" v-motion :initial="{opacity:0}" :click-6="{opacity:1}">[] <span class="ml-2 text-xs">— loop ends</span></div>
</div>

<div class="text-xs opacity-55 mt-4 mb-1">out <span class="opacity-70">— one entry per wave</span></div>
<div class="space-y-0.5">
  <div class="dgab-t font-bold" v-motion :initial="{opacity:0,x:-40}" :click-3="{opacity:1,x:0}">[rg]</div>
  <div class="dgab-t font-bold" v-motion :initial="{opacity:0,x:-40}" :click-4="{opacity:1,x:0}">[storage]</div>
  <div class="dgab-t font-bold" v-motion :initial="{opacity:0,x:-40}" :click-5="{opacity:1,x:0}">[files, cdn]</div>
  <div class="dgab-t font-bold" v-motion :initial="{opacity:0,x:-40}" :click-6="{opacity:1,x:0}">[hello]</div>
</div>

</div>

</div>

<!--
- (bonus) That loop's three variables, live. `ready` is a wave.
-->

---
routeAlias: II_13
zoom: 1.0
---

# Step 4 — run it

<Window title="zsh — byoiac" kind="terminal" maxHeight="335px">

<div v-click="1">

```console
$ rm -f state.json                    # delete the state, rerun
$ python src/4-graph/engine.py up
```

</div>
<div v-click="2">

```console
  + create rg
  + create storage
  + create files
  + create hello
```

</div>
<div v-click="3">

```console
  + rg
```

</div>
<div v-click="4">

```console
  + storage                           # 21 seconds polling for up
  + files
  + hello
```

</div>

</Window>

<!--
- Run it.
- ⏱ ~20s of real dead air between `+ rg` and `+ storage`. ▶ Flip back one slide and walk `ordered()` and the poller. Return when the shell prints.
-->

---
routeAlias: II_13b
layout: center
class: text-center
---

# We're back up

<div class="flex justify-center mt-4">
<div style="max-width:620px">
<Window title="byoiacdemo2026.blob.core.windows.net/files/hello.html" kind="editor">
<img src="./images/live-page.png" alt="the deployed page, live" />
</Window>
</div>
</div>

<!--
- Run it. The page is back — we're back up.
- ▶ Browser, not portal. Open the URL. Public, phones welcome.
- ⚠️ Right after a fresh account create the URL can 404 for a few seconds (blob DNS propagation). Narrate the graph while it settles. Verified 200 within ~2s on a warm account (2026-08-31).
- ⏱ ~20 seconds.
-->

---
routeAlias: II_15
zoom: 1.0
---

# Step 4 — and back down, reversed

<Window title="zsh — byoiac" kind="terminal" maxHeight="335px">

<div v-click="1">

```console
$ python src/4-graph/engine.py destroy
  - delete rg
  - delete storage
  - delete files
  - delete hello
```

</div>
<div v-click="2">

```console
  - hello
  - files
  - storage
  - rg
```

</div>

</Window>

<!--
- And teardown is the same list, reversed.
- ▶ `up` again NOW (restores state for Step 5) while talking.
-->

---
routeAlias: II_15b
layout: center
---

# You are here

<div class="text-xl leading-snug font-mono mt-2">

<div class="whitespace-nowrap"><span class="opacity-50 mr-5">1</span><b>cli</b><span class="opacity-60 ml-5">— a script driving a tool</span></div>
<div class="whitespace-nowrap"><span class="opacity-50 mr-5">2</span><b>api</b><span class="opacity-60 ml-5">— the same script, raw HTTP</span></div>
<div class="whitespace-nowrap"><span class="opacity-50 mr-5">3</span><b>state</b><span class="opacity-60 ml-5">— store the state, derive the diff</span></div>
<div class="whitespace-nowrap"><span class="opacity-50 mr-5">4</span><b>graph</b><span class="opacity-60 ml-5">— store the arrows, derive the order</span><span class="text-orange-500 font-bold ml-5">◀ you are here</span></div>
<div v-click class="opacity-35 whitespace-nowrap"><span class="mr-5">5</span>?</div>
<div v-click class="opacity-35 whitespace-nowrap"><span class="mr-5">6</span>?</div>
<div v-click class="opacity-35 whitespace-nowrap"><span class="mr-5">⋮</span></div>
<div v-click class="opacity-35 whitespace-nowrap"><span class="mr-5">N</span>?</div>

</div>

<!--
- So how much further is there? Four rungs named, the rest blank.
- ▶ click ×4: 5, 6, ⋮, N. Let the unnamed rungs land in silence. Don't name them, the not-knowing IS the setup.
-->

---
routeAlias: III_0
---

# What if someone changes something manually?

<IaCSandbox />

<!--
- But what if something changes? Delete a row behind its back and it says *no changes*. A belief you never re-check is just a memory.
- ▶ LIVE. ✕ a row in Cloud. Be the person who opens the portal. Hit `up` → **"no changes."** Let that sit.
- ▶ `refresh` → the row drops out of State → `up` → it comes back.
- ▶ `+ portal`: someone else creates `legacy-1`. `up` → **"no changes"** again. Blind to vanishing AND to arriving. (That unmanaged row is why `import` exists. Notice there's no button for it.)
- ⏱ ~2 min. Also the wifi fallback: this needs no cloud. The engine doesn't have `refresh` yet. The toy is previewing the question, and the code catches up over the next few slides.
-->

---
routeAlias: III_4
zoom: 0.85
---

# Refresh: what we wrote, and what came back

<div class="grid grid-cols-[2fr_3fr] gap-4 items-start">
<div class="min-w-0">

<Window title="infra.yaml — storage" kind="editor">

```yaml
storage:
  type: Microsoft.Storage/storageAccounts
  properties:
    location: eastus
    sku: {name: Standard_LRS}
    kind: StorageV2
    tags: {env: demo}
    properties:
      allowBlobPublicAccess: true
```

</Window>

</div>
<div class="min-w-0">

<Window title="zsh — byoiac" kind="terminal" maxHeight="400px">

```console
$ curl -H "Authorization: Bearer $TOKEN" \
    "https://management.azure.com/…/storageAccounts/byoiacdemo2026"
```

<div v-click="1">

```json
{
  "sku":  { "name": "Standard_LRS", "tier": "Standard" },
  "kind": "StorageV2",
  "location": "eastus",
  "tags": { "env": "demo" },
```

</div>
<div v-click="2">

```json
  "id": "/subscriptions/.../storageAccounts/byoiacdemo2026",
  "name": "byoiacdemo2026",
  "type": "Microsoft.Storage/storageAccounts",
```

</div>
<div v-click="3">

```json
  "properties": {
    "provisioningState": "Succeeded",
    "creationTime": "2026-08-13T16:05:05.2686429Z",
    "keyCreationTime": { "key1": "...", "key2": "..." },
    "primaryEndpoints": { "blob": "...", "dfs": "...", "file": "...",
                          "queue": "...", "table": "...", "web": "..." },
```

</div>
<div v-click="4">

```json
    "primaryLocation": "eastus",
    "statusOfPrimary": "available",
    "accessTier": "Hot",
    "minimumTlsVersion": "TLS1_0",
    "supportsHttpsTrafficOnly": true,
    "allowBlobPublicAccess": false,
    "allowCrossTenantReplication": false,
    "privateEndpointConnections": [],
    "networkAcls": { "defaultAction": "Allow", "bypass": "None", "ipRules": [] },
    "encryption": { "keySource": "Microsoft.Storage",
                    "services": { "blob": {}, "file": {} } }
  }
}
```

</div>

</Window>

</div>
</div>

<!--
- So just ask the cloud. One curl.
- ⏱ THE TURN, ~minute 30. Slow down.
- ▶ Four clicks, each a chunk of the response: (1) the fields we sent, plus a `tier` we didn't. (2) identity Azure invented. (3) `properties` begins: timestamps, endpoints. (4) the rest of the wall. Read it slowly. The response _is_ the slide.
-->

---
routeAlias: III_3
---

# We sent 7. Azure answered with 48.

<div class="mt-4">

| | fields we **PUT** | fields the **GET** returns |
|---|---|---|
| resource group | 2 top-level (`location`, `tags`) · 4 keys total | 6 top-level · **9 keys total** |
| storage account | 5 top-level (`location`, `tags`, `sku`, `kind`, `properties`) · 7 keys total | 8 top-level · **48 keys total** |

</div>

<!--
- We sent 7 fields. Azure answered with 48.
-->

---
routeAlias: III_2
zoom: 1.0
---

# Step 5 — ask the cloud what is actually there

<Window title="zsh — byoiac" kind="terminal" maxHeight="335px">

<div v-click="1">

```console
$ python src/5-cliff/engine.py refresh
```

</div>
<div v-click="2">

```console
  = rg: cloud returned 6 top-level fields; we own 2
  = storage: cloud returned 8 top-level fields; we own 4
  = files: cloud returned 5 top-level fields; we own 1
  = hello: the data plane just answers with the bytes
```

</div>

</Window>

<!--
- So `refresh` is one GET per resource — and the moment it learns the cloud has opinions.
-->

---
routeAlias: III_5
---

# Manually tracking what's owned

<Window title="src/5-cliff/engine.py" kind="editor">

```py {1-6|8-9}{lines:true}
OWNED = {  # per resource type: the properties that are OURS to manage
    "Microsoft.Resources/resourceGroups": ["location", "tags"],
    "Microsoft.Storage/storageAccounts": ["location", "tags", "sku", "kind"],
    "Microsoft.Storage/storageAccounts/blobServices/containers": ["properties"],
    "blob": ["contentType", "content"],
}

def owned(res):  # our declared properties, minus anything not ours to manage
    return {k: v for k, v in res["properties"].items() if k in OWNED[res["type"]]}
```

</Window>

<!--
- The fix is an allowlist: six hand-written lines, for four types out of two thousand.
-->

---
routeAlias: III_6
---

# Tracking shape

<div class="text-xl mb-2">We sent this:</div>

```json
"sku": { "name": "Standard_LRS" }
```

<div class="text-xl mt-4 mb-2">Azure returned this:</div>

```json
"sku": { "name": "Standard_LRS", "tier": "Standard" }
```

<div v-click>

<Window title="src/5-cliff/engine.py" kind="editor">

```py
def project(shape, actual):  # trim the cloud's answer to the shape we sent
    if isinstance(shape, dict) and isinstance(actual, dict):
        return {k: project(v, actual[k]) for k, v in shape.items() if k in actual}
    return actual                       # (sku comes back with a tier we never sent)
```

</Window>

</div>

<!--
- The fix is an allowlist: six hand-written lines, for four types out of two thousand.
- But even a field we own comes back reshaped, so names aren't enough.
- ⏱ 30 seconds, no more.
-->

---
routeAlias: III_7
layout: center
---

# Practical Problem

<div class="mt-8"></div>

## The loop was a hundred lines.

## The schemas are the millions.

<div v-click class="mt-10 text-xl opacity-90">

Which fields are mine · which are the server's · which are read-only · which come back reshaped

</div>

<!--
- **The loop was a hundred lines. The schemas are the millions.**
-->

---
routeAlias: III_9
---

# Step 6 — drift, done right

<Window title="src/6-drift/engine.py" kind="editor">

```py {4-7|8-10}{lines:true}
def refresh(state):
    for key in list(state):
        res = state[key]["res"]
        code, actual = call("GET", url_for(res))
        if code == 404:                 # deleted behind our back: forget it,
            print(f"  ! {key} vanished — deleted outside of us")
            del state[key]              # and the next plan will offer to rebuild
            continue
        was, now = state[key]["saved"], project(owned(res), actual)
        print(f"  {'~' if was != now else '='} {key}")
        state[key]["saved"] = now
```

</Window>

<!--
- The loop was a hundred lines. The schemas are the millions.
- And now the cliff buys us drift: changed → heal, vanished → rebuild.
-->

---
routeAlias: III_10
zoom: 1.0
---

# Someone edits behind our back

<Window title="zsh — byoiac" kind="terminal" maxHeight="360px">

<div v-click="1">

```console
$ az group update -n byoiac-demo --set tags.env=HACKED   # changed behind our back
$ python src/6-drift/engine.py plan
  no changes.
```

</div>
<div v-click="2">

```console
$ python src/6-drift/engine.py refresh
  ~ rg
  = storage
  = files
  = hello
```

</div>
<div v-click="3">

```console
$ python src/6-drift/engine.py plan
  ~ update rg
```

</div>
<div v-click="4">

```console
$ python src/6-drift/engine.py up
  ~ update rg
  ~ rg
```

</div>

</Window>

<!--
- So change a tag from outside. `plan` lies → `refresh` looks → `plan` tells the truth → `up` heals.
- ▶ The first `plan` says "no changes" — state is a belief, nobody told it.
-->

---
routeAlias: III_12
zoom: 1.0
---

# Someone deletes behind our back

<Window title="zsh — byoiac" kind="terminal" maxHeight="430px">

<div v-click="1">

```console
$ az group delete -n byoiac-demo --yes --no-wait   # the whole stack, gone
$ python src/6-drift/engine.py plan
  no changes.
```

</div>
<div v-click="2">

```console
$ python src/6-drift/engine.py refresh
  ! rg vanished — deleted outside of us
  ! storage vanished — deleted outside of us
  ! files vanished — deleted outside of us
  ! hello vanished — deleted outside of us
```

</div>
<div v-click="3">

```console
$ python src/6-drift/engine.py plan
  + create rg
  + create storage
  + create files
  + create hello
```

</div>
<div v-click="4">

```console
$ python src/6-drift/engine.py up      # ~23s — rebuilt from nothing
```

</div>

</Window>

<div v-click="5" class="mt-2 text-lg">

Using `OWNED`, we can keep `refresh` working for our specific types.

</div>

<!--
- Then delete everything from outside. It notices, and rebuilds from nothing — and only because of the cliff.
- ⏱ final `up` ≈ 23s. Start it, advance to the sandbox slide and talk over it.
- ▶ END of live demo after this. Slides and the toy only from here.
-->

---
routeAlias: III_12c
layout: center
---

# You are here

<div class="text-xl leading-snug font-mono mt-2">

<div class="whitespace-nowrap"><span class="opacity-50 mr-5">1</span><b>cli</b><span class="opacity-60 ml-5">— a script driving a tool</span></div>
<div class="whitespace-nowrap"><span class="opacity-50 mr-5">2</span><b>api</b><span class="opacity-60 ml-5">— the same script, raw HTTP</span></div>
<div class="whitespace-nowrap"><span class="opacity-50 mr-5">3</span><b>state</b><span class="opacity-60 ml-5">— store the state, derive the diff</span></div>
<div class="whitespace-nowrap"><span class="opacity-50 mr-5">4</span><b>graph</b><span class="opacity-60 ml-5">— store the arrows, derive the order</span></div>
<div v-click class="whitespace-nowrap"><span class="opacity-50 mr-5">5</span><b>cliff</b><span class="opacity-60 ml-5">— know which fields are yours</span></div>
<div v-click class="whitespace-nowrap"><span class="opacity-50 mr-5">6</span><b>drift</b><span class="opacity-60 ml-5">— re-check the belief</span></div>
<div v-click class="whitespace-nowrap"><span class="opacity-35 mr-5">7</span><span class="opacity-35">?</span><span class="text-orange-500 font-bold ml-5">◀ you are here</span></div>
<div class="opacity-35 whitespace-nowrap"><span class="mr-5">⋮</span></div>
<div class="opacity-35 whitespace-nowrap"><span class="mr-5">N</span><span>?</span></div>

</div>

<!--
- Two rungs cashed, and the list did not get shorter.
- ▶ Click 3: the arrow lands on 7, still unnamed. "The list did not get shorter. Here's the next one."
- ⏱ ~20s, then straight into the one-word change.
-->

---
routeAlias: III_18
---

# Next problem

<div class="text-xl mb-4">Change one word in <code>infra.yaml</code>:</div>

<Window title="infra.yaml" kind="editor">

````md magic-move
```yaml
  storage:
    type: Microsoft.Storage/storageAccounts
    name: byoiacdemo2026
    properties:
      location: eastus
```
```yaml
  storage:
    type: Microsoft.Storage/storageAccounts
    name: byoiacdemo2026
    properties:
      location: westus2
```
````

</Window>

<div v-click class="mt-8 text-3xl">

What should `up` do?

</div>

<!--
- Next problem: change one word. What should `up` do? — you just deleted an account with blobs in it.
- ▶ ASK THE ROOM: "what should `up` do?" Actually pause. Only audience question in the deck.
-->

---
routeAlias: III_18b
zoom: 0.9
---

# Replace, in place, or swap?

<div class="text-xl leading-relaxed mt-4">

One diff can be satisfied three different ways, and the tool has to pick:

</div>

<div class="text-xl leading-relaxed mt-6 space-y-4">

<div v-click><b>update in place</b> — PUT the change, the way our engine does. That works for a tag, but no PUT can move a region.</div>

<div v-click><b>delete, then create</b> — always works, and your storage account is <i>offline in between</i>.</div>

<div v-click><b>create, then switch</b> — build the new one, move traffic, delete the old. No downtime, but the name is taken, so the new one needs a <i>different name</i>.</div>

<div v-click><b>…and it cascades</b> — whatever depends on the replaced thing may have to rebuild too, in reverse dependency order.</div>

</div>

<!--
- Next problem: change one word. What should `up` do?
- Because one diff has three legal answers, and it cascades. Per-property metadata again.
-->

---
routeAlias: III_19
hide: true
layout: center
class: text-center
---

# Now make it worse

<div class="text-2xl mt-8 opacity-80">the storage account has a pinned name, so you cannot create the new one first</div>

<!--
- → Pinned name ⇒ can't create-first ⇒ delete first ⇒ every dependent goes too.
- ⏱ One breath, setup for the flurry.
-->

---
routeAlias: III_20
hide: true
---

# What the plan actually has to say

<Window title="pulumi preview" kind="terminal">

<div v-click="1">

```console
  ~ storage       replace  [location: eastus => westus2]
```

</div>
<div v-click="2">

```console
  - files         delete   (depends on storage)
```

</div>
<div v-click="3">

```console
  - hello         delete   (depends on files)
```

</div>
<div v-click="4">

```console
  - hello-2       delete   (depends on files)
```

</div>
<div v-click="5">

```console
  - storage       delete-before-replace
```

</div>
<div v-click="6">

```console
  + storage       create   westus2
```

</div>
<div v-click="7">

```console
  + container     create
```

</div>
<div v-click="8">

```console
  + hello         create
```

</div>
<div v-click="9">

```console
  + hello-2       create
```

</div>
<div v-click="10">

```console
  ! storage       pending delete — create failed, ghost lives in state
```

</div>

</Window>

<div v-click="11" class="mt-4 text-2xl">

**Pulumi computes this correctly every run, and you didn't even know it was a thing.**

</div>

<!--
- ▶ GO FAST: ~4s per click, zero explanation. It should feel like too much.
- 🗣 (landing) "Pulumi computes this correctly every run, and you didn't even know it was a thing."
- ⛔ Never reveal auto-naming. (Q&A pocket answer only.)
-->

---
routeAlias: III_21
hide: true
---

# Same picture. One edge.

<TriangleFocus focus="ps">

· which changes update, and which secretly **replace**

· unknown values — *known after apply*

· rename a variable without deleting the database

· one program, or twenty stacks referencing each other

</TriangleFocus>

<!--
- 🗣 "This edge, your code against what we remember. We wrote it as three list comprehensions."
- → Every line here is per-property or per-type knowledge. None of it is algorithm.
- ⏱ ~30s. Brisk. Do not explain any single item.
-->

---
routeAlias: III_22
hide: true
---

# Same picture. The other edge.

<TriangleFocus focus="sc">

· seven fields out, forty-eight back

· normalization — case, ordering, reshaped values

· *ready* is not *accepted* — polling, timeouts, per type

· soft-delete, purge, things that refuse to be deleted

· retries, throttling, eventual consistency

· **import** — adopt what we didn't create

</TriangleFocus>

<!--
- 🗣 "And this edge, what we remember against what's actually there. That was `refresh`. Twelve lines."
- → This is where the cliff lives. They've already felt it, so just name the family.
- ⏱ ~30s.
-->

---
routeAlias: III_23
hide: true
---

# Same picture. The file in the corner.

<TriangleFocus focus="state">

· secrets — outputs include passwords

· two engineers, one state file — that's why remote state and locking exist

· versioning, rollback, audit, recovery

· a format that still opens in three years

</TriangleFocus>

<div class="mt-6 text-xl">

The same diagram, the same three questions. **That is the 1%, and it is all of the work.**

</div>

<!--
- 🗣 "Same diagram all three times. The picture never got more complicated. The labels did."
- → The locking line is the whole race problem in one item. Q&A pocket (see `demo.md`, the race section): two `up`s three seconds apart, both exit zero, and state ends up asserting resources Azure is mid-delete. The five-line `O_EXCL` fix is in `src/6-drift/engine.py`'s `main()` if anyone asks to see it.
- 🗣 (land) "That's the one percent. And it's all of the work."
- ⏱ ~30s, then straight into the close.
-->

---
routeAlias: III_24
---

# And Azure was the easy cloud

<div class="text-lg mt-2 mb-4 opacity-80">We leaned on one mercy: <b>Azure is uniform</b> — one auth, PUT everywhere.</div>

| | auth | ordering | errors |
|---|---|---|---|
| **Azure** | one token | PUT everywhere | uniform |
| **AWS** | per-service signing | "created" before it's true | different shapes per service |
| **GCP** | long-running ops | poll every create | quota / project gates |
| **Kubernetes** | already desired-state | reconcile a reconciler | eventual, never "done" |

<!--
- And Azure was the easy cloud.
-->

---
routeAlias: III_8
layout: center
---

# We built 99% of the *idea* —

<div class="mt-2 mb-8 text-base opacity-70">an afternoon well spent</div>

<div class="w-full max-w-3xl">

<div class="text-sm mb-2 opacity-80">how complete it <b>feels</b></div>
<div class="flex w-full h-12 rounded overflow-hidden text-sm font-bold">
  <div class="flex items-center justify-center" style="width: 96%; background: #3b82f6; color:#fff;">■ state · diff · reconcile · graph</div>
  <div class="flex items-center justify-center" style="width: 4%; background: #f59e0b; color:#fff;">▲</div>
</div>

<div v-click>

<div class="text-sm mt-8 mb-2 opacity-80">how the <b>work</b> is actually distributed</div>
<div class="flex w-full h-12 rounded overflow-hidden text-sm font-bold">
  <div class="flex items-center justify-center" style="width: 4%; background: #3b82f6; color:#fff;">■</div>
  <div class="flex items-center justify-center" style="width: 96%; background: #f59e0b; color:#fff;">▲ schemas × 2,000 types · replace rules · parallel applies · unknowns · retries · partial failure</div>
</div>

</div>

</div>

<div v-click class="mt-10 text-2xl">

**— and 1% of the work.**

</div>

<!--
- So: 99% of the idea, 1% of the work.
-->

---
routeAlias: III_8d
---

# That 1%, up close

<div class="grid grid-cols-2 gap-10 mt-6">

<div>

<div class="text-lg dgbb-t font-semibold mb-3">Our engine — every resource, one shape</div>

```python
# create / update
call("PUT",    url_for(res), res["properties"])
# read
call("GET",    url_for(res))
# destroy
call("DELETE", url_for(res))
```

<div class="mt-5 text-lg opacity-80">
Every Azure resource is a <strong>URL</strong> you
<code>PUT</code> / <code>GET</code> / <code>DELETE</code>.
<br>That uniformity <em>is</em> the engine.
</div>

</div>

<div>

<div class="text-lg dgab-t font-semibold mb-2">azure-native · KeyVault <code>AccessPolicy</code></div>

<div class="text-base opacity-90 leading-snug">

<div v-click class="mb-2">⬦ It <strong>isn't a resource.</strong> Azure has no PUT/GET/DELETE for one policy — it's a slice of the vault.</div>

<div v-click class="mb-2">⬦ <strong>read</strong> = GET the entire vault, loop every policy hunting for your <code>objectId</code>.</div>

<div v-click class="mb-2">⬦ <strong>create vs. update?</strong> Azure only offers "Replace." So the provider reads first and <em>fakes the distinction itself.</em></div>

<div v-click class="mb-2">⬦ <strong>delete</strong> = a "Remove" op on the parent vault.</div>

<div v-click class="mb-2">⬦ permissions: 4 categories, hand-marshalled <strong>both directions</strong> (~70 lines).</div>

<div v-click class="mb-2">⬦ the ID shape changed once — and can <strong>never</strong> change again, or every import breaks. It carries both formats forever.</div>

</div>
</div>

</div>

<div v-click class="mt-3 text-center text-xl dgab-t font-semibold">
~340 lines. For a thing with three fields.
</div>

<div class="mt-4 text-center text-sm opacity-55">
all 15 of these live here →
<a href="https://github.com/pulumi/pulumi-azure-native/tree/v3.27.0/provider/pkg/resources/customresources"><code>pulumi-azure-native / …/ customresources</code></a>
</div>

---
routeAlias: IV_1
---

# So: use Pulumi <span class="text-2xl font-normal opacity-45">— or Terraform, or OpenTofu</span>

<div class="grid grid-cols-2 gap-4">

<div>

<div class="text-lg mb-1 opacity-70">ours — infra.yaml</div>

```yaml
resources:
  rg:
    type: Microsoft.Resources/resourceGroups
    name: byoiac-demo
    properties:
      location: eastus
      tags: {env: demo, talk: kcdc}

  storage:
    type: Microsoft.Storage/storageAccounts
    name: byoiacdemo2026
    resourceGroup: byoiac-demo
    dependsOn: [rg]
    properties:
      location: eastus
      sku: {name: Standard_LRS}
      kind: StorageV2
      tags: {env: demo}
```

</div>

<div>

<div class="text-lg mb-1 opacity-70">real Pulumi YAML</div>

```yaml
resources:
  rg:
    type: azure-native:resources:ResourceGroup
    properties:
      resourceGroupName: byoiac-demo
      location: eastus
      tags: {env: demo, talk: kcdc}

  storage:
    type: azure-native:storage:StorageAccount
    properties:
      accountName: byoiacdemo2026
      resourceGroupName: ${rg.name}

      location: eastus
      sku: {name: Standard_LRS}
      kind: StorageV2
      tags: {env: demo}
```

</div>

</div>

<!--
- So use a real one. And you delete a line when you graduate: `${rg.name}` is the edge, so `dependsOn` is gone.
-->

---
routeAlias: IV_3
hide: true
---

# State. Diff. Reconcile.

<div class="text-2xl mt-6 opacity-80">a hundred lines, and now you know how all of them work</div>

<div v-click class="text-2xl mt-10 opacity-80">everything after that is per-resource knowledge someone else already paid for</div>

<!--
- 🗣 "State. Diff. Reconcile. A hundred lines. Everything after that is per-resource knowledge someone else already paid for."
- → End calm: relief, not fear. Two slides left: the invitation, then the QR.
-->

---
routeAlias: IV_3b
layout: center
---

<style>
.byox { --am:#f59e0b; --bl:#3b82f6; text-align:center; line-height:1.02; max-width:960px; margin:0 auto; }
.byox span { display:inline-block; margin:.14em .36em; white-space:nowrap; font-weight:600; background:none; border:none; }
.byox .am { color:var(--am); }
.byox .bl { color:var(--bl); }
.byox .d1{opacity:.9} .byox .d2{opacity:.62} .byox .d3{opacity:.42}
.byox .hero { color:var(--am); font-weight:800; border-bottom:3px solid var(--am); }
</style>

# Build your own *everything*

<div class="byox mt-5" style="font-size:1rem">
<span class="hero" style="font-size:2.3em">an IaC tool</span>
<span class="bl" style="font-size:1.6em">a shell</span>
<span class="d1" style="font-size:2em">a database</span>
<span class="d2" style="font-size:1.25em">git</span>
<span class="am" style="font-size:1.5em">a compiler</span>
<span class="d1" style="font-size:2.2em">an operating system</span>
<span class="d3" style="font-size:1.1em">a regex engine</span>
<span class="bl" style="font-size:1.35em">a ray tracer</span>
<span class="d2" style="font-size:1.65em">a text editor</span>
<span class="d1" style="font-size:1.2em">a garbage collector</span>
<span class="am" style="font-size:1.85em">a virtual machine</span>
<span class="d2" style="font-size:1.25em">Docker</span>
<span class="d3" style="font-size:1.1em">a bloom filter</span>
<span class="bl" style="font-size:1.6em">a game engine</span>
<span class="d1" style="font-size:1.35em">a key-value store</span>
<span class="d2" style="font-size:1.2em">a Lisp</span>
<span class="am" style="font-size:1.45em">a TCP/IP stack</span>
<span class="d2" style="font-size:1.75em">a web server</span>
<span class="d3" style="font-size:1.1em">a JSON parser</span>
<span class="bl" style="font-size:1.3em">a DNS server</span>
<span class="d1" style="font-size:1.5em">a neural network</span>
<span class="d3" style="font-size:1.2em">Redis</span>
<span class="am" style="font-size:1.35em">a search engine</span>
<span class="d2" style="font-size:1.3em">an emulator</span>
<span class="d3" style="font-size:1.1em">a template engine</span>
<span class="bl" style="font-size:1.4em">a spreadsheet</span>
</div>

<!--
- So use a real one.
- But build your own *everything* anyway. The idea fits in an afternoon; the cliff is the payoff; that's when you're allowed to stop.
- ▶ Just the visual. Say it: the idea fits in an afternoon (fun + learning), the cliff always comes (that's the payoff — now you can read the real one), and that's when you stop. Don't run it in prod.
-->

---
routeAlias: IV_2
zoom: 0.88
---

# Exercise for the reader

<Window title="Program.cs" kind="editor">

```csharp
using Pulumi;
using Pulumi.AzureNative.Resources;
using Pulumi.AzureNative.Storage;
using Pulumi.AzureNative.Storage.Inputs;

return await Deployment.RunAsync(() =>
{
    var rg = new ResourceGroup("rg", new ResourceGroupArgs
    {
        ResourceGroupName = "byoiac-demo",
        Location = "eastus",
        Tags = { { "env", "demo" }, { "talk", "kcdc" } },
    });

    var storage = new StorageAccount("storage", new StorageAccountArgs
    {
        AccountName = "byoiacdemo2026",
        ResourceGroupName = rg.Name,
        Location = "eastus",
        Sku = new SkuArgs { Name = SkuName.Standard_LRS },
        Kind = Kind.StorageV2,
        Tags = { { "env", "demo" } },
    });
});
```

</Window>

<!--
- The same program in C#.
-->

---
routeAlias: IV_4
layout: center
class: text-center
---

# Thanks!

<div class="flex items-start justify-center gap-16 mt-10">

<div class="text-center">
  <img src="/images/adam.png" class="w-36 h-36 rounded-full object-cover mx-auto mb-3" />
  <div class="text-xl font-bold">Adam Gordon Bell</div>
  <div class="text-base opacity-60">Pulumi</div>
  <div class="mt-2 text-sm opacity-70 space-y-1 text-left inline-block">
    <div class="flex items-center gap-2"><carbon-logo-x /> @adamgordonbell</div>
    <div class="flex items-center gap-2"><carbon-cloud /> @adamgordonbell.bsky.social</div>
  </div>
</div>

<div class="text-center">
  <div class="bg-white rounded-lg p-2 inline-block shadow-lg">
    <img src="/images/repo-qr.png" class="w-36 h-36" alt="Repo QR" />
  </div>
  <div class="mt-2 text-base opacity-80">The code + this talk</div>
  <div class="text-sm opacity-50 font-mono">github.com/adamgordonbell/<br>build-your-own-iac</div>
</div>

<div class="text-center">
  <div class="bg-white rounded-lg p-2 inline-block shadow-lg">
    <img src="/images/pulumi-qr.png" class="w-36 h-36" alt="Pulumi profile QR" />
  </div>
  <div class="mt-2 text-base opacity-80">My writing at Pulumi</div>
  <div class="text-sm opacity-50 font-mono">pulumi.com/blog/author/<br>adam-gordon-bell</div>
</div>

</div>

<!--
- Thanks.
- ▶ After stage: `destroy`, rm state files. Repo went public 2026-09-01. Both QRs verified live.
-->

---
routeAlias: IV_5
layout: center
class: text-center
---

# Feedback

<div class="mt-10">
  <div class="bg-white rounded-lg p-3 inline-block shadow-lg">
    <img src="/images/kcdc-feedback-qr.png" class="w-56 h-56" alt="KCDC session feedback QR" />
  </div>
  <div class="mt-4 text-xl opacity-80">KCDC session feedback</div>
  <div class="mt-1 text-base opacity-50">Every submission enters the closing raffle</div>
</div>

<!--
- Feedback.
-->
