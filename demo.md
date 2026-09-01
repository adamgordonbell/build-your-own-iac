# Run of show — "Build Your Own IaC"

KCDC 2026, 1-hour breakout. Every command below was run against real Azure on
2026-08-13, updated 2026-08-31; the outputs are transcripts, not guesses.

**Shell setup (do this before you walk on stage, then again at the podium):**

```bash
cd ~/sandbox/build-your-own-iac
az login                                            # token lives ~1 hour — refresh at the podium
export AZURE_SUBSCRIPTION_ID=$(az account show --query id -o tsv)
az account show --query name -o tsv                 # say the sub name out loud once
az storage account check-name --name byoiacdemo2026 --query nameAvailable
rm -f state.json state.lock                         # start from nothing
```

If `check-name` returns `false`, someone took the name between now and the talk.
Edit the `byoiac*` name in every `src/*/infra.yaml`, in `src/2-api/deploy.py`
and in `src/1-cli/deploy.sh` (3–24 lowercase alphanumerics) and re-run — the
`deploy.sh` copy is on a slide, so it has to match. Do this at rehearsal, not at
the podium.

**Layout:** one folder per step under `src/` — `1-cli 2-api 3-state
4-graph 5-cliff 6-drift`, each named for the concept that step keeps
(the old `7-race` lockfile folded into `6-drift` 2026-09-01 — ~5 lines;
the short-lived `4-flat` folded into `3-state` later the same day: step 3 now
manages the full stack, no ordering — its crash on the tidied file opens
Beat 4). `1-cli` is `deploy.sh`, the `az`
script — **slide only, never run on stage.** `2-api` is `deploy.py`, the
raw-REST version, and that one does run. The rest are each a complete
copy of the engine as of that beat. **Always run from the repo root**
(`python src/N-x/engine.py …`): `state.json` lands in the root and carries
across beats. Moving between beats is just typing a different path — nothing to
check out, nothing to revert. To show what a beat *added*, diff neighbors:
`diff src/3-state/engine.py src/4-graph/engine.py`.

## Timing

60-minute slot. Beat times are the per-beat estimates in the headings below;
the open and the ending are estimates (marked est.) — everything else has been
paced against the measured wall-clocks quoted in each beat.

| Segment | Min | Notes |
|---|---|---|
| Cover + problem slide + stack diagram (`I_1`–`I_2b`) | 2 est. | Title, the promise, the page in a browser window, then the nested four-objects diagram (`I_2b`, no clicks). Don't linger. |
| **Beat 2** — script, curtain-pull, run, payoff stills, two failures + we-got-lucky + delete-ledger, two questions, diff-pivot, desired-state yaml, matching problem (`I_3`–`II_3`) | 10 | Includes ~26s + ~23s of live run and the fire-and-forget teardown. New slides 2026-08-31: `II_1b` payoff stills (~10s), `II_2a` we-got-lucky (~60s, **cuttable**), `II_2b2` delete-ledger (~60s). |
| **Beat 3** — the whole tool: state code, reconcile code, vocabulary slide, one full-stack run, page-back payoff, line-count slide (+ sandbox visits 1 and 2) | 12 est. | Restructured 2026-09-01: step 3 manages the FULL stack (114 lines). One from-empty run (`up` 26.4s measured incl. the sleep-20 shrug · `up` · `cat state.json` · edit+`plan`+`up`), NO destroy (page stays up for `II_9b` payoff; Beat 4's crash slide destroys). Transcripts captured live 2026-09-01. Re-time at rehearsal. |
| **Beat 4** — order-by-failure open, Go aside, small example, the graph, the page returns, the poller | 9 est. | ~21–23s of live poll, filled deliberately. Opening reworked 2026-09-01 (twice — bridge slide deleted; failing engine IS step 3): `II_10b3` tidy magic-move + `II_10c` destroy→up crash (repro: `src/3-state` + `infra-tidied.yaml`) + `II_10d` Go aside (cuttable) + `II_10e` four-names example, ~+2 min. New close: `II_15b` "You are here" ladder (~30s). |
| **Beat 5** — the cliff (opens with sandbox visit 3, "What if something changes?") | 10 est. | The turn. Reordered 2026-09-01: toy question (~2 min, moved in from Beat 6) → cover → raw `curl` reveal → table → `refresh` implementation → `OWNED`. |
| **Beat 6** — drift | 5 est. | Two outside-world CLI one-liners (`az group update` tag edit at `III_9b`; `az group delete` ~60s fire-and-forget at `III_11`), each followed by plan/refresh/plan/up. No portal driving. Sandbox visit 3 moved to the top of Beat 5 (2026-09-01) — re-time both beats at rehearsal. |
| Ending sequence (ladder revisited `III_12c` ~20s, "Next problem" + `III_18b` replace-moves ~2min, other-clouds `III_24`, 99%/1% bars, "So: use Pulumi" `IV_1` ~60s (the ONE Pulumi slide; C# `IV_2` hidden), `IV_3b` build-your-own-everything, `IV_4` thanks+QR) | 6 est. | Slimmed 2026-09-01: flurry (`III_19`/`III_20`) and roll-call triangles (`III_21`–`III_23`) hidden via `hide: true`, not deleted. New: `III_18b`, reworked `III_24`, `IV_3b`, `IV_4` (QR → repo — ⚠️ repo must be public before the talk). |
| **Total** | **53 est.** | Beats 3 (11), 4 (9), 5 (10), 6 (5), and the ending (5) are estimates — re-sum after rehearsal times them. |

**Slack: ~5 minutes against 60** (pending real timing on the estimated beats). That is
the overrun budget — not spare content. Two live segments (Beats 2 and 4) can
each lose a minute to Azure without touching the plan, and there is now roughly
a short Q&A's worth left over if everything runs clean.

**If you are running long, squeeze in this order — trim, don't cut:**

1. **`II_2a` we-got-lucky** — cut the whole slide; the story survives without
   it (~60s). It's first because it's a pure aside.
2. **`II_10d` the Go/Python dict aside** — same reasoning (~45s); the failure
   and the four-names example carry the beat without it.
3. **Beat 5's cliff walk** — show the 48-key GET and `OWNED`, skip reading the
   trimmed JSON aloud and drop the `sku`/`project()` second verse (~90s).
4. **Beat 6's live group delete (6b)** — narrate the vanished case off the
   `refresh` output instead of doing the ~60s delete live (~2 min).

Items 3–4 are squeezes, not cuts: they stay in the deck and in this file.
The race beat is already out of the talk (see the Q&A pocket below).

---

## Beat 2 — The dumb deploy script (`src/1-cli` on a slide, `src/2-api` live) · ~10 min

**The scenario, said out loud before anything is on screen:** I have a web page.
It needs to be on the internet. I could click through the Azure portal for ten
minutes — but I'm smarter than that, so I script it.

**Slide (10 seconds, don't read it aloud):** `src/1-cli/deploy.sh` — five `az`
commands. Group, storage account, container, upload, print the URL. Everyone in
the room has written this file. **It is never run on stage** — it exists so the
room recognises itself, and so the raw-REST version lands as a reveal rather than
a curiosity. Then the curtain-pull: *every one of those commands is one HTTP
request.* Here they are.

**Slide:** `src/2-api/deploy.py` on screen — ~50 lines, no SDK, no framework,
`import urllib`. Four PUTs, top to bottom, and a `time.sleep(20)` in the middle
because storage takes a while and 20s is usually enough. Then run it.

```bash
python src/2-api/deploy.py
```

```
PUT https://management.azure.com/subscriptions/<sub>/resourcegroups/byoiac-demo
  -> 201
PUT https://management.azure.com/subscriptions/<sub>/resourceGroups/byoiac-demo/providers/Microsoft.Storage/storageAccounts/byoiacdemo2026
  -> 202
sleeping 20s for the storage account...
PUT https://management.azure.com/subscriptions/<sub>/resourceGroups/byoiac-demo/providers/Microsoft.Storage/storageAccounts/byoiacdemo2026/blobServices/default/containers/files
  -> 201
POST https://management.azure.com/subscriptions/<sub>/resourceGroups/byoiac-demo/providers/Microsoft.Storage/storageAccounts/byoiacdemo2026/listServiceSas
  -> 200
PUT https://byoiacdemo2026.blob.core.windows.net/files/hello.html
  -> 201

your page: https://byoiacdemo2026.blob.core.windows.net/files/hello.html
```

**~26s wall clock** (2026-08-31, real run). Twenty of those are the sleep — fill
them by walking the four PUTs on screen: the container is still ARM, just a
deeper URL; the file is the data plane, a different API with different auth, but
*still a PUT*, with a signature the management plane hands us.

**The payoff (browser, not portal):** open
`https://byoiacdemo2026.blob.core.windows.net/files/hello.html`. A deployed web
page in minute five, public, phones welcome. ⚠️ Right after a fresh account
create the URL can 404 for a few seconds (blob DNS propagation) — narrate the
last PUT while it settles; verified 200 on the first curl (2026-08-31). See
rehearsal checklist.

**The line:** that's the whole job. So why does anybody need Terraform?

### The script's two failures

**Failure one — run it again.**

```bash
python src/2-api/deploy.py
```

```
PUT .../resourcegroups/byoiac-demo
  -> 200
PUT .../storageAccounts/byoiacdemo2026
  -> 200
sleeping 20s for the storage account...
PUT .../blobServices/default/containers/files
  -> 200
POST .../listServiceSas
  -> 200
PUT https://byoiacdemo2026.blob.core.windows.net/files/hello.html
  -> 201

your page: https://byoiacdemo2026.blob.core.windows.net/files/hello.html
```

**~23s again.** It "worked" — 200s instead of 201s, because PUT is an upsert, so
nothing broke. But it re-sent everything, and it still sat there for twenty
seconds doing nothing, for a page that was already exactly right. Point at the
blob's `201`: even that last line has no idea it just overwrote itself.

**The aside (`II_2a`, slide only, ~60s, first thing to cut if long):** we only
got away with that because ARM's PUT is create-or-update — rerunning was safe
*by accident*. On AWS half the APIs split Create-X from Update-X, so a script
has to ask what exists before it can pick a verb. Land the foreshadow: check
what's out there, then decide what to send — hold that thought, we're about to
do it on purpose.

**Failure two — narrate this one, no need to run it.** Open `deploy.py` on the
slide and delete the container and blob stanzas — the page is no longer wanted.
Run it. Nothing happens. The resource group and the storage account get PUT
again, and the file is still sitting on the internet. Nothing happens, and
*nothing can happen*: a script only says "make this exist." There is no line you
can add to a script like this that means "get rid of the thing I asked for
yesterday," because the script has no idea what it asked for yesterday.

**The obvious fix (`II_2b2`, slide only, ~60s):** fine — add a `DELETE` line.
It even works, once. But now *removing* something means *adding* a line, and
that line can never be removed, because who knows which machines already ran
the script. Six months in it's creates on top, a graveyard of deletes below,
re-deleted on every run: a log of actions nobody can read the system from.
Don't say "state" yet — the questions slide is next.

**Two questions, and they drive the rest of the hour:**

1. How do you do nothing when nothing changed?
2. How do you delete?

**Stage note — clearing the script's mess:** Beat 2 leaves a real resource group,
storage account, container and blob behind, and no tool knows about any of it.
Beat 3 starts the tool over at rg-only, so the script's stack has to go first.
Fire and forget: while the two-questions slide is up, run

```bash
az group delete -n byoiac-demo --no-wait --yes   # ~60s with storage inside; fire it and keep talking
```

and keep narrating. `--no-wait` returns immediately; Azure finishes in the
background over the next minute or so, which is roughly how long the two
questions and the ownership diagram take. Give it that beat before Beat 3 —
Beat 3's first `up` re-creates the resource group, and if that PUT lands while
the delete is still in flight, ARM returns 409. The drill is: wait ten seconds,
run it again. ⚠️ see rehearsal checklist — the 409-on-race is expected ARM
behavior, but this sequence has not been captured live.

---

## Beat 3 — The tool: state → reconcile (`src/3-state`) · ~12 min · **line-count slide + sandbox visit 2**

One step, one engine file, three code slides, **one run at the end**. Slide one
shows the state slice of `engine.py` (the pillar-1 section — two functions and
the save-as-you-go lines); slide two shows `diff` + `apply` from the same file;
slide three (`II_6b`) shows `url_for` — the vocabulary. The loop only runs once
it's whole. (Restructured 2026-09-01: step 3 now manages the FULL stack — the
old rg-only intermediate was folded away so every step from 2-api on is a
working solution to "deploy the page.")

**Start over.** The script's stack is gone, there is no `state.json` yet. The
tool we build deploys the same four things the script did — but this time it
remembers.

**Code slide 1 (state):** the memory — `load_state`/`save_state` and the
save-as-you-go lines, excerpted from the one engine file. This is the answer to
"how do you delete?" The script had no idea what it asked for yesterday — so
give the tool a memory, and record `saved` (what we sent) while you're at it.
Don't run anything yet: keep building.

**Code slide 2 (reconcile):** `diff` decides, `apply` acts. Desired minus state
gives three sets — create, update, delete. That is the entire content of every
progress bar you have ever watched. (The slide excerpt is trimmed — the real
`apply` also branches for the blob and keeps the script's `sleep(20)` shrug.)

**Code slide 3 (vocabulary, `II_6b`):** `url_for` — the script's URLs folded
into one function, the ONLY type-specific code in the tool. The blob keeps its
data-plane detour (SAS), the `sleep(20)` shrug survives verbatim. All of
deploy.py is in the engine now.

**The run** (real captures, live against Azure 2026-09-01):

```bash
python src/3-state/engine.py up
```
```
  + create rg
  + create storage
  + create files
  + create hello
  + rg
  + storage
  + files
  + hello
```

**26.4s measured** — the long gap after `+ storage` is the script's inherited
`sleep(20)`. Narrate it: twenty seconds of guessing, fixed next beat.

```bash
python src/3-state/engine.py up          # again
```
```
  no changes.
```

Run two sent nothing, instantly — no re-PUTs, no twenty seconds burned on a
stack that was already right. The script couldn't have done that: with no
memory there was nothing to compare against. Doing nothing is a feature, and it
costs a memory and a subtraction.

```bash
cat state.json
```

There's the memory — four entries, including `saved`, what we sent. And it is a
*belief*, not a fact. Nothing checked. Everything painful about IaC comes from
the gap between that belief and the cloud.

Edit `src/3-state/infra.yaml`: change `talk: kcdc` to `talk: kcdc2026` —
⚠️ the tag lives in an inline dict (`tags: {env: demo, talk: kcdc}`), edit in
the editor, not sed.

```bash
python src/3-state/engine.py plan       # ~ update rg   — nothing sent
python src/3-state/engine.py up
```
```
  ~ update rg
  ~ rg
```

**The pivot line:** `plan` called zero write APIs — it compared two dicts and
printed the difference. `up` printed the same line and then meant it. Plan and
apply are the same subtraction; only one of them phones the cloud.

**Portal:** refresh the resource group's Tags blade — `talk` is now `kcdc2026`.
Revert the edit and `up` again to put it back.

**The payoff (`II_9b` — browser, not portal):** open
`https://byoiacdemo2026.blob.core.windows.net/files/hello.html`. The page is
back — deployed by a tool that knows what it made. That was the promise at the
top of the hour. ⚠️ Fresh-account 404 window applies (see rehearsal checklist).
**No destroy here** — the stack stays up; Beat 4's crash slide tears it down as
its clean-slate step.

**The line:** name the three pieces now, looking back at what we built, not
forward at what's coming. A memory of what we made. A subtraction that turns two
descriptions into three sets. A loop that walks the sets and calls the API —
state, diff, reconcile. 114 lines against the script's fifty, and both
questions answered — and the page is back. That is a working IaC tool, and now
you know how all of them work. The rest of the hour is the part nobody puts on
a slide.

---

## Beat 4 — Dependency graphs (`src/4-graph`) · ~9 min

132 lines. Order gets introduced by failure, not assertion (opening reworked
2026-09-01 twice: the failing engine IS step 3 — the bridge slide is gone;
slides `II_10b3`–`II_10e`):

**1. The tidy (`II_10b3`, magic-move, no prose).** hello.html is the star of
the file — someone moves it to the top. Why not? The file is a picture, not a
recipe. Say nothing while the block slides up. The reordered file is checked in
as `src/3-state/infra-tidied.yaml`.

**2. Run it (`II_10c`).** `destroy` first (clean slate — tears down Beat 3's
full stack), then `cp src/3-state/infra-tidied.yaml src/3-state/infra.yaml`
and `up`: the diff prints happily (`+ create` ×4 — the diff doesn't know about
order), then the blob PUT fires first and dies with `TypeError: 'NoneType'
object is not subscriptable`. The cloud said 404; the traceback names nothing.
Punchline on the slide: **the tool created things in file order — and that
won't scale.** Both transcripts are real captures (2026-09-01, live). A design
decision hides in the destroy: file-order deletes (rg first) crashed for real —
the rg cascade killed the account before the blob delete could sign its SAS —
so the engine tears down with `reversed(deletes)` ("teardown = setup order,
backwards", one word of borrowed luck; Beat 4's `reversed(ordered())` is what
it grows into). Crash line 62 confirmed. The `up` from empty state creates
nothing — no cleanup needed. Restore afterwards: `git checkout
src/3-state/infra.yaml`.

**3. The fun aside (`II_10d`, ~45s, cuttable second after `II_2a`).** Python
dicts iterate in insertion order (guaranteed since 3.7) — the bug is invisible,
you ship it. Go randomizes map iteration *on purpose* — this engine written in
Go fails loudly the first afternoon. Terraform is written in Go; not a
coincidence they were free to ignore. But the fix isn't a stricter language.

**4. The problem, small (`II_10e`).** Four names, three arrows (→ means
*needs*). hello·rg·storage·files crashes; rg·storage·files·hello works — and so
does any order that respects the arrows. The arrows are the truth; order is
derived. **Store arrows, derive order.**

**5. Write it down (`II_11`).** The file already has all four wishes — what it
gains is three lines: `dependsOn: [rg]`, `dependsOn: [storage]`,
`dependsOn: [files]`. The order the script encoded in its line numbers, now
described rather than commanded (`diff src/3-state/engine.py
src/4-graph/engine.py` = the whole feature: `ordered()` + `wait_ready`). Then
`II_11b` names the seam: the container is still ARM — just a deeper URL; the
file is the data plane, a different API but *still a PUT*, with a SAS the
management plane signs for us (`listServiceSas`). Plant the flag: "remember
this edge — uniformity just ended, and it's going to matter."

**Point at `dependsOn:` and say what it replaced.** The script had this too. It
was the order of the lines. On the `ordered()` slide, walk the small example
through `visit()`: start anywhere — Go-map order, alphabetized, hello-first —
the derived order is the same. Nothing can scramble it.

```bash
rm -f state.json
cat src/4-graph/infra.yaml              # point at the dependsOn chain
python src/4-graph/engine.py up
```
```
  + create rg
  + create storage
  + create files
  + create hello
  + rg
  + storage
  + files
  + hello
```

**The payoff (`II_13b`, browser, not portal):** open
`https://byoiacdemo2026.blob.core.windows.net/files/hello.html` — the page is
back **and not by luck**: the order was derived from the arrows, not inherited
from the file; reordering can't scramble it. (The big promise-kept moment
already landed at `II_9b` in Beat 3 — this one is specifically the ordering
victory.) Public, phones welcome. ⚠️ Right after a fresh account create the URL
can 404 for a few seconds (blob DNS propagation) — narrate the graph while it
settles; verified 200 within ~2s on a warm account (2026-08-31). See rehearsal
checklist.

**Measured timings (say these out loud while it runs):**

| | PUT returns | ready (`provisioningState: Succeeded`) |
|---|---|---|
| resource group | **201** in 1.2s | 1.4s |
| storage account | **202 Accepted** in 2.7s | **20.8s** |
| whole `up` | | **~21–23s** |

**~20 seconds of dead air.** Fill it deliberately: this is the eventual-consistency
beat. 202 means "I have written down that you want this"; the resource does not
exist yet, and `wait_ready` is polling every 2s. Call it back — remember the
`sleep(20)` in the script, with the shrug of a comment next to it saying twenty
seconds is usually enough? This is what it turns into once you're not guessing:
ask the resource whether it's ready, and go when it says yes. Same twenty
seconds today, but it's twenty seconds of *knowing*, and on a bad day it's forty
and the tool still works. Walk the audience through
`ordered()` on screen while the poller spins — parents first on the way up,
children first on the way down, five lines of depth-first search.

Then:

```bash
python src/4-graph/engine.py destroy
```
```
  - delete rg
  - delete storage
  - delete files
  - delete hello
  - hello
  - files
  - storage
  - rg
```

Point at the order: reversed — the file dies before its container, the
container before its account. Then `up` again to restore for Beat 5.

**The line:** the moment there are two resources, the desired state is a graph,
not a list. Note `dependsOn:` — remember that line, it disappears at the end.

**Then the ladder (`II_15b`, ~30s):** "You are here" — steps 1–4 named with
their concepts, arrow at 4, then four clicks reveal `5 ? · 6 ? · ⋮ · N ?`
unnamed. Don't name them; let the not-knowing sit. It's the breather before the
turn, and the cliff answers the question the blank rungs just asked.

---

## Beat 5 — **The cliff** (`src/5-cliff`) · ~8 min · **the turn of the talk**

159 lines. Reworked 2026-09-01: the beat now opens with the *question* (drift,
in the toy), reveals the answer with a raw `curl` — **before** any engine code —
and only then implements `refresh`.

**1. The toy poses it (`III_0`, ~2 min):** sandbox visit 3, full toy, titled
"What if something changes?" ✕ a Cloud row → `up` says **no changes** → let it
sit → `refresh` previews the answer. Name the fork: **undo it** (yaml wins) or
**adopt it** (reality wins, pull it into state) — either way, step one is asking
the cloud what's actually there. `+ portal` for the arriving case. Wifi
fallback too.

**2. The raw answer (`III_4`). This is the slide — and the turn; slow down.** Our seven-line description
on the left; one `curl` — not our engine, the API itself — on the right:

```bash
TOKEN=$(az account get-access-token --query accessToken -o tsv)
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://management.azure.com/subscriptions/$AZURE_SUBSCRIPTION_ID/resourceGroups/byoiac-demo/providers/Microsoft.Storage/storageAccounts/byoiacdemo2026?api-version=2023-05-01" \
  | python -m json.tool
```

**3. Quantify it (`III_3`)**, then **4. implement `refresh` (`III_2`)**:

```bash
python src/5-cliff/engine.py refresh
```
```
  = rg: cloud returned 6 top-level fields; we own 2
  = storage: cloud returned 8 top-level fields; we own 4
  = files: cloud returned 5 top-level fields; we own 1     (re-captured 2026-09-01)
  = hello: the data plane just answers with the bytes
```

### The measured cliff (2026-08-13, real response)

| | fields we **PUT** | fields the **GET** returns |
|---|---|---|
| **resource group** | 2 top-level (`location`, `tags`) · 4 keys total | 6 top-level · **9 keys total** |
| **storage account** | 5 top-level (`location`, `tags`, `sku`, `kind`, `properties`) · 7 keys total | 8 top-level · **48 keys total** |

**We sent 7. Azure answered with 48.** (7 = the 5 top-level fields plus sku.name and the nested allowBlobPublicAccess. re-verified live 2026-09-01: 8 top-level / 48 total keys.) A naive `desired != actual` diff would
propose "fixing" 42 fields nobody asked for — several of which are read-only and
will 400 if you try.

Trimmed response (the 14 keys under `properties`, none of which we sent):

```json
{
  "sku":  { "name": "Standard_LRS", "tier": "Standard" },   ← we sent name; tier is theirs
  "kind": "StorageV2",
  "location": "eastus",
  "tags": { "env": "demo" },
  "id": "/subscriptions/.../storageAccounts/byoiacdemo2026",
  "name": "byoiacdemo2026",
  "type": "Microsoft.Storage/storageAccounts",
  "properties": {
    "provisioningState": "Succeeded",
    "creationTime": "2026-08-13T16:05:05.2686429Z",
    "keyCreationTime": { "key1": "...", "key2": "..." },
    "primaryEndpoints": { "blob": "...", "dfs": "...", "file": "...",
                          "queue": "...", "table": "...", "web": "..." },
    "primaryLocation": "eastus",
    "statusOfPrimary": "available",
    "accessTier": "Hot",
    "minimumTlsVersion": "TLS1_0",
    "supportsHttpsTrafficOnly": true,
    "allowBlobPublicAccess": false,
    "allowCrossTenantReplication": false,
    "privateEndpointConnections": [],
    "networkAcls": { "defaultAction": "Allow", "bypass": "None",
                     "ipRules": [], "ipv6Rules": [], "virtualNetworkRules": [] },
    "encryption": { "keySource": "Microsoft.Storage",
                    "services": { "blob": {...}, "file": {...} } }
  }
}
```

Then show the fix on screen — `OWNED`, 4 lines:

```python
OWNED = {
    "Microsoft.Resources/resourceGroups": ["location", "tags"],
    "Microsoft.Storage/storageAccounts": ["location", "tags", "sku", "kind"],
}
```

**The second verse, worth 30 seconds:** even `sku` — a field we *do* own — comes
back as `{"name": "Standard_LRS", "tier": "Standard"}` when we sent only `name`.
An allowlist of *field names* isn't enough; you also have to compare shape-wise.
That's `project()`, and it exists because of one property on one resource type.

**The line:** the uniformity that let us build the loop in ~100 lines does exactly
nothing here. Which fields are mine, which are the server's, which are read-only,
which come back reshaped — that is per-property, per-resource-type knowledge.
Azure has ~2,000 resource types. Then do it again for AWS. **The loop was 100
lines. The schemas are the millions.** That is the product.

---

## Beat 6 — Drift (`src/6-drift`) · ~7 min

179 lines. Two kinds of drift, both live — and the lockfile (folded in from
the old race step). Both cases follow the same on-stage pattern (2026-09-01):
one outside-world CLI line in a "not our tool" window, then plan/refresh/
plan/up. No portal driving.

### 6a — changed

**On stage (slide `III_9b`):** one line, run live, instant:

```bash
az group update -n byoiac-demo --set tags.env=HACKED -o none
```

```bash
python src/6-drift/engine.py plan       # no changes.        ← state still believes
python src/6-drift/engine.py refresh    # ~ rg / = storage / = files / = hello
python src/6-drift/engine.py plan       # ~ update rg        ← now it sees it
python src/6-drift/engine.py up         # ~ rg               ← healed
```

Optionally show the portal Tags blade back at `env: demo` as proof — but as an
exhibit, not a control panel.

### 6b — vanished

**On stage (slide `III_11`, reworked 2026-09-01):** not the portal — the slide
shows the nuke line and you RUN it, fire-and-forget, same trick as Beat 2's
teardown:

```bash
az group delete -n byoiac-demo --yes --no-wait
```

**Timing:** a resource group *containing the storage account* takes **~60s** to
delete. Fire the delete, then talk through `refresh()` on screen for a minute
before running the commands. Do not stand there watching the spinner.

```bash
python src/6-drift/engine.py plan       # no changes.        ← state still believes
python src/6-drift/engine.py refresh
```
```
  ! rg vanished — deleted outside of us
  ! storage vanished — deleted outside of us
  ! files vanished — deleted outside of us
  ! hello vanished — deleted outside of us
```
```bash
python src/6-drift/engine.py plan
```
```
  + create rg
  + create storage
  + create files
  + create hello
```
```bash
python src/6-drift/engine.py up         # ~23s — rebuilt from nothing
```

**The line:** notice this beat is only possible *because* of Beat 5. Without
`OWNED`, every `refresh` would scream drift on 42 fields nobody touched and the
one real change would be buried. Normalization isn't a detail — it's what makes
drift detection mean anything.

---

## Q&A pocket — the race (cut from the talk; the lock now lives in `src/6-drift`)

**Not in the run of show.** The beat is cut; the code ships to attendees and one
roll-call line covers it on stage ("two engineers, one state file — that's why
remote state exists"). What follows is here in case someone asks and there is
time to run it. Budget ~6 min if you take it; it is not in the 53.

Two people, one state file. (Since 2026-09-01 the lock lives in `src/6-drift`
itself, so the lockless version for the failure demo is `src/5-cliff` — same
engine minus drift detection and the lock.)

Show the failure first with `src/5-cliff` — no lock (this is reproducible —
the ~21s storage window makes the interleaving reliable):

```bash
python src/6-drift/engine.py destroy; sleep 20; rm -f state.json

# Alice runs up; Bob runs destroy three seconds later
( python src/5-cliff/engine.py up ) &  ( sleep 3; python src/5-cliff/engine.py destroy ) &  wait
```

Both exit 0. Both look fine. Then:

```bash
python -c "import json; print(list(json.load(open('state.json')).keys()))"
# ['rg', 'storage', 'files', 'hello']     ⚠️ see rehearsal checklist
az group show -n byoiac-demo --query properties.provisioningState -o tsv
# Deleting
```

**The state file asserts two resources that Azure is in the middle of deleting.**
Bob's `destroy` read state before Alice had recorded the storage account, so it
deleted the resource group out from under her; Alice then wrote a state file
describing a world that no longer exists. Next `plan` says "no changes."

Now the lock — five lines, right in `src/6-drift/engine.py`'s `main()`:

```python
try:  # O_EXCL is atomic — "check then create" would be a race of its own
    lock = os.open(LOCK_FILE, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
except FileExistsError:
    raise SystemExit(f"state is locked by another run (rm {LOCK_FILE} if stale)")
os.write(lock, str(os.getpid()).encode())
```

```bash
rm -f state.json state.lock
( python src/6-drift/engine.py up ) & ( sleep 2; python src/6-drift/engine.py up ) & wait
```
```
  + create rg
  + create storage
  + rg
  + storage
state is locked by another run (rm state.lock if stale)
```

**The line:** note that even the *lock* had a race in it — check-then-create is
itself two operations. That's why real tools don't put state in a file next to
your code; they put it behind something that can do a compare-and-swap. Remote
state and state locking aren't enterprise upsell. They're the first bug you hit
with two engineers.

---

## Ending (slides only — never run a second live tool) · ~7 min est.

The sequence: replace-vs-update (`III_18b`), the other-clouds list, the 99%/1%
bars, then the `infra.yaml` vs real Pulumi YAML diff.
Callback for the close: **`dependsOn: [rg]` from Beat 4 — in Pulumi you write
`${rg.name}` and delete that line, because the graph falls out of the reference.**

---

## Cleanup — do this before you leave the stage

The talk ends at Beat 6, so `src/6-drift` owns the live state file. (Beat 2's
script stack was already torn down by the `az group delete --no-wait` in Beat
2's stage note; Beat 6 rebuilt the same resource group under the tool.)

```bash
python src/6-drift/engine.py destroy
rm -f state.json state.lock          # 6-drift takes the lock on every run
```

Verify (should print nothing / error out):

```bash
az group show -n byoiac-demo -o tsv
az storage account check-name --name byoiacdemo2026 --query nameAvailable   # true
```

---

## Reset to replay from scratch

```bash
cd ~/sandbox/build-your-own-iac
python src/6-drift/engine.py destroy 2>/dev/null   # if state.json exists
az group delete -n byoiac-demo --yes   # belt and braces; catches the `2-api` stack too, ~60s if storage is inside
rm -f state.json state.lock
export AZURE_SUBSCRIPTION_ID=$(az account show --query id -o tsv)
```

The `az group delete` is the one that matters after a partial replay: `src/2-api`
has no state and no `destroy`, so anything it made is only reachable by name.

Full replay cost: ~4 min of Azure wall-clock — three `up`s at ~21–23s, the two
`deploy.py` runs at ~26s and ~23s, and two ~60s group deletes (Beat 2's teardown
and Beat 6b's `az group delete`) — plus whatever you spend in the portal.

## Failure drills

| If | Then |
|---|---|
| `KeyError: 'AZURE_SUBSCRIPTION_ID'` | you opened a new terminal — re-export it |
| 401 from ARM mid-talk | token expired; `az login` and re-run, the command is idempotent |
| Beat 3's first `up` returns **409** | the Beat 2 `az group delete --no-wait` is still in flight; wait ten seconds and run it again (verified live 2026-09-01: `ResourceGroupBeingDeleted`, cleared in ~45s) |
| `deploy.py` dies with **409** at the container PUT | the 20s sleep wasn't enough — seen live 2026-09-01 on a cold account. Just run it again: PUTs are upserts, the second run completed in ~22s. It's even on-message ("that's the shrug failing") |
| Beat 2's page 404s in the browser | blob DNS hasn't propagated; keep narrating the PUTs, reload after ~10s |
| storage name taken | edit the `byoiac*` name in every `src/*/infra.yaml`, in `src/2-api/deploy.py` (line 17) and in `src/1-cli/deploy.sh` (the slide), `rm state.json`, re-run |
| conference wifi dies | fall back to the asciinema recordings; the RG-only path (Beat 3) is the light one |
| `up` hangs past ~60s | `wait_ready` is polling a resource that failed; Ctrl-C, check the portal |
| `state is locked` | a previous run died holding the lock (any `6-drift` verb) — `rm state.lock` |

---

## Rehearsal checklist

Every open verification item in one place. The inline ⚠️ markers in this file
and in `slides/slides.md` point here. Nothing on this list is a known bug — it
is output that was captured before the current stack existed, or behavior that
has not been watched live yet.

**Transcripts to re-capture (invariant 3 — real output only, never composed)**

1. ~~**Beat 5 `refresh`, the `files` line.**~~ **DONE 2026-09-01** — live run
   against the four-resource stack: `files: cloud returned 5 top-level fields`.
   Filled in here and on deck slide `III_2`.
3. ~~**Beat 5 cliff GET key count.**~~ **DONE 2026-09-01** — re-measured live:
   SA 8 top-level / **48 total keys** (14 under `properties`), RG 6 / 9. The
   2026-08-13 numbers still hold exactly; deck slide `III_3` is correct as is.
3. ~~**Deck slide `III_10`.**~~ **DONE 2026-09-01** — full sequence re-run live
   (tag drifted via `az group update` standing in for the portal): refresh
   prints `~ rg / = storage / = files / = hello`; plan `~ update rg`; up healed
   the cloud tag back to `demo`. Slide updated.
4. **Q&A pocket (the race).** The `state.json` keys transcript has not been
   re-captured since the file beat landed. Only matters if the pocket ever gets
   used; do it if there is time left at rehearsal.

**Behavior to watch live once**

5. ~~**Beat 2 → Beat 3 409 race.**~~ **DONE 2026-09-01** — run in sequence for
   real: `up` 10s after the fire-and-forget delete returns
   `409 ResourceGroupBeingDeleted`, exactly as the slide warns; the delete
   finished in ~45–60s and the retry then succeeded. The drill works.
5b. ~~**Beat 3's merged run**~~ (deck slide `II_9`) **DONE 2026-09-01** — whole
   sequence run in one sitting with the real file edit: `up` (from empty) →
   `up` (no changes.) → edit `talk: kcdc → kcdc2026` in the editor →
   `plan` (`~ update rg`) → `up` (`~ rg`, cloud tag confirmed `kcdc2026`) →
   `destroy`. Matches the slide's transcripts line for line. (Tag is inside an
   inline dict — still edit in the editor, not sed.)
6. **The 404 window on a fresh account.** Both Beat 2 and Beat 4 open the page
   right after a create. Verified 200 on the first curl (Beat 2) and within ~2s
   warm (Beat 4), but neither was watched in a browser on a cold account —
   check how long the blob DNS gap really is and whether the narration covers it.

**Stage feel — decide at rehearsal, no right answer in advance**

7. **Deck slide `I_4` scrolls.** The `deploy.py` code window shows roughly 22 of
   59 lines per stage. Judge on the room: acceptable, or does it need splitting?
8. **Beat 2's second run.** Failure one costs another ~23s of wall clock. Decide
   whether to run it live or narrate it over the first run's transcript slide.
   Running it is more honest; narrating it buys back most of a minute.

**Standing pre-talk items**

9. **Storage-account name re-check, the week of the talk.** `az storage account
   check-name --name byoiacdemo2026`; if it's gone, see the rename drill in the
   setup section above.
10. ~~Flip the GitHub repo public~~ **DONE 2026-09-01** — verified 200 logged-out; both `IV_4` QRs live.
11. **Record the asciinema fallbacks** at rehearsal — the wifi-dies drill has
    nothing to fall back to until this is done.
12. **Full live re-verification pass of every beat** under the folder layout.
    Still owed; every item above piggybacks on it rather than needing its own
    session.
