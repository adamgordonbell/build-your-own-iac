# Build Your Own IaC — running the demo

One folder per step under `src/`, each a complete copy of the tool as of that
step. **Always run from the repo root** — `state.json` lands in the root and
carries across steps. Moving between steps is just typing a different path.

## Setup (once per session)

```bash
cd ~/sandbox/build-your-own-iac
az login                                            # token lasts ~1 hour
export AZURE_SUBSCRIPTION_ID=$(az account show --query id -o tsv)
az storage account check-name --name byoiacdemo2026 --query nameAvailable
```

If `check-name` returns `false`, the name is taken — change `byoiac*` in every
`src/*/infra.yaml`, `src/2-api/deploy.py`, and `src/1-cli/deploy.sh`, then re-run.

## The steps

Each engine takes a verb: `plan` (default), `up`, `destroy`; `5-cliff` and
`6-drift` also take `refresh`.

```bash
# 1 — cli:   the az script (this one is on a slide; run with the shell, not python)
./src/1-cli/deploy.sh

# 2 — api:   the same thing as raw REST, no SDK
python src/2-api/deploy.py

# 3 — state: store the state, derive the diff
python src/3-state/engine.py up
python src/3-state/engine.py plan
python src/3-state/engine.py destroy

# 4 — graph: store the arrows, derive the order
python src/4-graph/engine.py up
python src/4-graph/engine.py destroy

# 5 — cliff: know which fields are yours
python src/5-cliff/engine.py up
python src/5-cliff/engine.py refresh
python src/5-cliff/engine.py plan

# 6 — drift: re-check the belief
python src/6-drift/engine.py up
python src/6-drift/engine.py refresh
python src/6-drift/engine.py plan
```

To see what a step added, diff neighbors:

```bash
diff src/3-state/engine.py src/4-graph/engine.py
```

## Reset / teardown

Everything lands in the `byoiac-demo` resource group, so one delete cascades the
storage account, container, and blob.

```bash
./reset.sh              # between runs: delete local state + the resource group (waits until gone)
./reset.sh --no-wait    # same, but don't block on the cloud delete

./teardown.sh           # just the cloud side (leaves state.json in place)
./teardown.sh --no-wait # fire-and-forget
```

The engines' own `destroy` verb also tears a step down cleanly; `reset.sh` is
the catch-all for switching steps or recovering from a half-built run.
