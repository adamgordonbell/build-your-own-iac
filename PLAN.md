# Build Your Own IaC — Demo Engine Plan

Code for the KCDC 2026 talk *"Demystifying the Magic: Let's Build an Infrastructure-as-Code Tool from Scratch"* (Wed–Fri Sep 9–11, 1-hr breakout, Architecture track). Prep record: `~/para/projects/kcdc-iac-talk/`.

**The promise:** a functional IaC engine in ~100 lines of Python implementing **state → diff → reconciliation**, hitting the hard-problem beats (dependency graphs, race conditions, drift) — and an ending that shows why the distance from this toy to a usable product is enormous, with Pulumi as the team that crossed it.

## Core decisions (settled 2026-08-13)

1. **Azure, not AWS.** KCDC is a Microsoft-shop-heavy room (the submitted description already says "Pulumi, Terraform, or Bicep"), and Azure Resource Manager's uniform REST surface is what makes the whole stunt possible in an hour.
2. **Raw REST, no SDK.** Stronger than the abstract's "no frameworks — just Boto3" claim: stdlib `urllib.request` + one bearer token. Every ARM resource is the same shape — `PUT` (idempotent upsert) / `GET` / `DELETE` on a resource ID. Token via `az account get-access-token` shell-out (client-credentials POST as fallback). ⚠️ The description's Boto3 line goes stale — one-line edit to send Gabby when the program text matters.
3. **Resources:** resource groups (instant, free, tag-updatable — the workhorse) + one storage account (real dependency edge on its resource group, and its LRO/202-poller is the eventual-consistency beat).
4. **Desired state = `infra.yaml`, shaped deliberately like Pulumi YAML** (`resources:` / `type:` / `properties:`). One dependency — `pyyaml`, one `safe_load` line — which *makes* the point that the input language is the shallowest layer of an IaC tool. Built this way from stage 0 so the closing slide is a *diff* against real Pulumi YAML, not a comparison (decided 2026-08-13).
5. **State file = local JSON** (`state.json`), printable on screen mid-demo.
6. **CLI verbs:** `up`, `plan`, `destroy`, `refresh` via `sys.argv`.
7. **The engine stays honest-small:** core loop ≤100 lines. Later stages visibly grow it — the growth is itself a beat.

## The two-part thesis (what the ending must prove)

- **The loop is easy.** Three pillars, one hour, uniform API. That's the satisfying teaching — real understanding of how every IaC tool works.
- **The product is hard.** Proven live by **the cliff** (stage 5): the same uniformity that let us build the loop does nothing for per-resource *semantics* — and that knowledge, at breadth, is the product.

## Build stages (each = talk beat = git tag)

| Stage | Tag | What gets built | Talk beat |
|---|---|---|---|
| 0 | `v0-token` | Bearer token + one raw `PUT` creates a resource group. Print the request. | "The cloud is just a REST API." Run it twice — idempotent, no failure… so why do we need anything more? |
| 1 | `v1-state` | `state.json`: record what we created; `up` skips known resources | Pillar 1: State — "what we *think* exists" (and why PUT-upsert isn't enough: deletes, renames) |
| 2 | `v2-diff` | Desired-vs-state → create/update/delete sets; `plan` prints without applying | Pillar 2: The Diff — the progress bar demystified |
| 3 | `v3-reconcile` | CRUD loop executes the diff; tag updates; `destroy` | Pillar 3: Reconciliation — a working IaC tool, ~100 lines. Line-count slide here. |
| 4 | `v4-deps` | Storage account + topo-sort of the two-node graph; its 202 + poller = async beat | Hard problem: dependency graphs (+ eventual consistency for free) |
| 5 | `v5-cliff` | `refresh` GETs actual state → **the cliff**: we sent 6 fields, Azure returns ~50; naive diff wants to "fix" 44 server-owned fields. Fix for *one* resource type: an `OWNED_FIELDS` allowlist. | **The turn.** Per-property, per-resource-type knowledge × ~2,000 ARM types × every cloud = the product. The loop was 100 lines; the schemas are the millions. |
| 6 | `v6-drift` | With normalization in hand, real drift detection: delete the RG in the portal mid-talk, `plan` catches it | Hard problem: drift — state vs reality, now done *right* |
| 7 | `v7-race` | Two concurrent `up`s corrupt state (pre-baked artifact); add a lockfile live (~5 lines) | Hard problem: race conditions → why remote state + locking exist |

## The ending sequence (after v7, asserted not built)

1. **Replace-vs-update beat** (~90 sec, one slide): edit `eastus` → `westus2` in `infra.py`, ask "what should `up` do?" — you can't move a region; the update is secretly **delete + create**, and that one word just deleted a storage account with its blobs. Knowing which properties do this is per-property metadata again (cliff, third verse).
2. **The cascade flurry slide** (deliberately too fast, ~4 sec/line): a pinned-name resource with a replace-forcing change → can't create-first (name collision) → delete-before-replace → cascades to every dependent in **reverse topological order** → plan output piles up (`~ replace` → `- - -` deletes → `+ + +` creates) → and if the create fails halfway, a pending-delete ghost lives in state for next run. Real engine behavior: [pulumi/pulumi#2167](https://github.com/pulumi/pulumi/issues/2167), years of plan-bookkeeping fixes ([#11009](https://github.com/pulumi/pulumi/pull/11009)). Landing line: **"Pulumi computes this correctly every run — and you didn't even know it was a thing."** ⛔ No auto-naming reveal (Adam, 2026-08-13) — the point is hidden complexity absorbed on your behalf, not the naming trick. (True mechanism, for Q&A: default auto-naming + create-first replacement is *why* nobody in the room has seen this plan.)
3. **The roll-call**: unknown values flowing through the graph, partial failure at resource 7 of 20, retries/throttling, secrets in state, previews you can trust — and Azure was the *easy* cloud; AWS speaks three protocols before breakfast. ⇒ Pulumi: Azure Native is generated from the same API specs we just called; the product is the team that ate the whole list.
4. **The language close** (~90 sec, static slides only — never run a second live tool): side-by-side **diff** of our `infra.yaml` vs the same two resources in real Pulumi YAML. Visible differences are exactly the right ones: `azure-native:storage:StorageAccount` vs our raw ARM type string, and `${rg.name}` where we wrote `dependsOn` — Pulumi infers the graph from references; you *delete a line* when you graduate. Then one slide: the same program in C# (this room) or Python — same desired state, same engine underneath; languages are generated frontends and YAML is just the simplest one. The `${rg.name}` reference doubles as the unknown-values callback. End here: complexity peaks at the flurry slide, resolves into "same infra, calm, handled" — relief, not fear.

Each stage is a tagged commit → deliverable as staged walkthrough (checkout tags) or live-code (type the diffs). Decision deferred to rehearsal; repo supports both.

## Repo layout

```
build-your-own-iac/
  PLAN.md          ← this file
  engine.py        ← the ~100-line engine (the artifact of the talk)
  infra.yaml       ← the "user program": desired state, Pulumi-YAML-shaped
  state.json       ← gitignored; created at runtime
  demo.md          ← run-of-show: exact commands + portal actions per beat
  README.md        ← for attendees who clone it after
```

## Risks / open questions

- **Auth on stage:** `az` token expiry mid-talk; refresh in the run-of-show right before going live. Fallback: asciinema recordings of every stage (record at rehearsal).
- **Conference wifi:** raw REST is light, but LRO polling on the storage account could stall. Fallback recordings cover it; resource-group-only path works offline-ish (fast, retry-friendly).
- **Which subscription:** personal/sandbox Azure sub, `byoiac-` name prefix, `destroy` closes the run-of-show so nothing leaks. Verify the sub exists and `az` works before stage 0.
- **Cliff field-count:** verify a vanilla resource group / storage account GET really returns the dramatic field spread (it should; confirm exact counts for the slide during the spike).
- **Line budget honesty:** raw REST + poller + topo-sort might land ~120–140 by v5. Fine — "about 100" covers v3; growth after v3 is a feature. But v3 itself must come in ≤100.

## Next actions

1. **Spike (stage 0–3):** token + RG CRUD end-to-end, `up`/`plan`/`destroy`, tag update. Verify ≤100 lines and capture the cliff field-count while there.
2. Stages 4–7 as additive tagged commits.
3. `demo.md` run-of-show; deck work then starts from it (deck lives in `~/para/projects/kcdc-iac-talk/`).
4. Queue the Boto3→"raw Azure REST" description edit for the next Gabby touchpoint.
