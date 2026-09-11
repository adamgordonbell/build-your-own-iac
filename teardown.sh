#!/usr/bin/env bash
# Tear down everything the demo created.
#
# Every step (cli, api, state, graph, cliff, drift) builds into the one
# resource group, so deleting it cascades the storage account, the container,
# and the blob. Blocks until the group is actually gone (so a re-run is clean);
# pass --no-wait to fire-and-forget instead.
set -euo pipefail

RG="${RG:-byoiac-demo}"

WAIT_FLAG=""
[[ "${1:-}" == "--no-wait" ]] && WAIT_FLAG="--no-wait"

if [[ "$(az group exists --name "$RG")" != "true" ]]; then
  echo "Resource group '$RG' does not exist — nothing to tear down."
  exit 0
fi

echo "Deleting resource group '$RG'..."
az group delete --name "$RG" --yes $WAIT_FLAG

if [[ -n "$WAIT_FLAG" ]]; then
  echo "Delete started in the background (~60s)."
else
  echo "Done — '$RG' is gone."
fi
