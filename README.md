# Build Your Own IaC

**A working Infrastructure-as-Code engine in 114 lines of Python** — raw Azure
REST, no SDK, no framework. Just `urllib`, a bearer token borrowed from `az`,
and one YAML parser. It deploys a resource group, a storage account, a public
container, and a real web page you can open in a browser. Then it grows, one
hard problem at a time, until it does dependency graphs, drift detection, and
locking in ~180 lines.

This is the code from the KCDC 2026 talk *"Demystifying the Magic: Let's Build
an Infrastructure-as-Code Tool from Scratch."* It exists to be read: every
folder under `src/` is the complete engine as of one step of the talk, and the
diff between neighbors shows what that step added.

## The idea

Every Azure resource is the same thing: `PUT` / `GET` / `DELETE` on a URL. So
an IaC tool is three pillars wrapped around that uniformity:

1. **State** — `state.json`, what we *think* exists.
2. **The diff** — desired (`infra.yaml`) minus state, giving create / update / delete.
3. **Reconciliation** — walk the diff and make the calls.

In `src/3-state/` that is **114 lines** — a tool that deploys the same page a
raw script did, and can also rerun, update in place, and tear down. Everything
after that is the hard problems.

## The steps

| Folder | Lines | What it adds |
|---|---|---|
| `src/1-cli` | 9 | `deploy.sh` — the five `az` commands you'd actually write. The starting point, not the engine. |
| `src/2-api` | ~50 | The same five commands as raw REST: a token and four PUTs deploy a real public web page. It works — but it can't tell when nothing changed, and can't delete anything. |
| `src/3-state` | **114** | The whole engine: state, diff, reconcile — plus the script's URL shapes and the blob SAS call. A working IaC tool, with one gap: resources are created in *file order*. `infra-tidied.yaml` is the same file reordered (`hello` moved first) — swap it in and `up` crashes. |
| `src/4-graph` | 132 | The fix: `dependsOn` in the file, an 11-line topological sort, and a 202 poller (`wait_ready` replaces the 20-second sleep). Parents first going up, children first coming down. |
| `src/5-cliff` | 159 | `refresh` — and the discovery that the API returns 48 fields for the 7 we sent. |
| `src/6-drift` | 179 | Real drift detection (changed, and vanished) — plus a five-line lockfile, because two people share one state file. |

Useful diffs:

```bash
cat src/3-state/engine.py                          # the whole engine in one file
diff src/3-state/engine.py src/4-graph/engine.py   # the whole "ordering" feature
diff src/4-graph/engine.py src/5-cliff/engine.py   # refresh, and the OWNED allowlist
```

## Try it

Requires Python 3.9+, `pip install pyyaml`, and the Azure CLI logged in
(`az login`). Everything it creates is cheap, and `destroy` takes it all back.

```bash
export AZURE_SUBSCRIPTION_ID=$(az account show --query id -o tsv)

# storage account names are globally unique — pick a free one
az storage account check-name --name byoiacdemo2026 --query nameAvailable
# if false, edit the byoiac* names in src/*/infra.yaml (3-24 lowercase alnum)

# run from the repo root — state.json lands here, shared across steps
python src/6-drift/engine.py plan       # what would change
python src/6-drift/engine.py up         # create everything (~22s; the storage account is async)
python src/6-drift/engine.py refresh    # ask the cloud what's actually there
python src/6-drift/engine.py destroy    # take it all back down
```

To reproduce the ordering crash from the talk, run step 3 against the tidied
file:

```bash
cp src/3-state/infra-tidied.yaml src/3-state/infra.yaml
python src/3-state/engine.py up          # crashes on the blob
git checkout src/3-state/infra.yaml
```

## Files

```
src/N-name/  one folder per step: engine.py (+ infra.yaml from step 3 on;
             steps 1 and 2 are the pre-engine scripts)
slides/      the deck (Slidev) — every terminal transcript in it is a real
             capture against Azure, not a mockup
demo.md      the run-of-show, if you want to give this talk yourself
state.json   created at runtime, gitignored — what the tool thinks exists
```

## Who made this

[Adam Gordon Bell](https://adamgordonbell.com) — developer relations at
[Pulumi](https://www.pulumi.com/), host of the
[CoRecursive podcast](https://corecursive.com). On X:
[@adamgordonbell](https://x.com/adamgordonbell) · Bluesky:
[@adamgordonbell.bsky.social](https://bsky.app/profile/adamgordonbell.bsky.social).
