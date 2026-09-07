# Build Your Own IaC
**A working Infrastructure-as-Code engine in 114 lines of Python.** Raw Azure REST, no SDK, no framework. Just `urllib`, a bearer token borrowed from `az`, and one YAML parser. It deploys a resource group, a storage account, a public container, and a real web page you can open in a browser. We start with the simplest thing that works and build up, one hard problem at a time, to dependency graphs, drift detection, and locking in about 180 lines.

This is the code from the KCDC 2026 talk _"Demystifying the Magic: Let's Build an Infrastructure-as-Code Tool from Scratch."_

Slides: [PDF export](./slides/build-your-own-iac-kcdc-2026.pdf), still a work in progress. To run the deck in a browser, `cd slides && pnpm install && pnpm dev`. The live deck has an interactive IaC sandbox that the PDF cannot show.
## The idea
Every Azure resource is the same thing: `PUT` / `GET` / `DELETE` on a URL. So an IaC tool is three pillars wrapped around that uniformity:

1. **State**: `state.json`, what we _think_ exists.
  
2. **The diff**: desired (`infra.yaml`) minus state, giving create / update / delete.
  
3. **Reconciliation**: walk the diff and make the calls.
  
## The steps
| Folder | Lines | What it adds |
|---|---|---|
| `src/1-cli` | 9 | `deploy.sh`, the five `az` commands you'd actually write. The starting point, not the engine. |
| `src/2-api` | ~50 | The same five commands as raw REST: a token and four PUTs deploy a real public web page. It works, but it can't tell when nothing changed, and can't delete anything. |
| `src/3-state` | **114** | The whole engine: state, diff, reconcile, plus the script's URL shapes and the blob SAS call. A working IaC tool, with one gap: resources are created in *file order*. `infra-tidied.yaml` is the same file reordered (`hello` moved first); swap it in and `up` crashes. |
| `src/4-graph` | 132 | The fix: `dependsOn` in the file, an 11-line topological sort, and a 202 poller (`wait_ready` replaces the 20-second sleep). Parents first going up, children first coming down. |
| `src/5-cliff` | 159 | `refresh`, and the discovery that the API returns 48 fields for the 7 we sent. |
| `src/6-drift` | 179 | Real drift detection (changed, and vanished), plus a five-line lockfile, because two people share one state file. |

Useful diffs:

```bash
cat src/3-state/engine.py                          # the whole engine in one file
diff src/3-state/engine.py src/4-graph/engine.py   # the whole "ordering" feature
diff src/4-graph/engine.py src/5-cliff/engine.py   # refresh, and the OWNED allowlist
```
## Try it
Requires Python 3.9+, `pip install pyyaml`, and the Azure CLI logged in (`az login`).

```bash
export AZURE_SUBSCRIPTION_ID=$(az account show --query id -o tsv)
# storage account names are globally unique, pick a free one
az storage account check-name --name byoiacdemo2026 --query nameAvailable
# if false, edit the byoiac* names in src/*/infra.yaml (3-24 lowercase alnum)
# run from the repo root; state.json lands here, shared across steps
python src/6-drift/engine.py plan       # what would change
python src/6-drift/engine.py up         # create everything (~22s; the storage account is async)
python src/6-drift/engine.py refresh    # ask the cloud what's actually there
python src/6-drift/engine.py destroy    # take it all back down
```
