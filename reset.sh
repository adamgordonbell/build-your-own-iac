#!/usr/bin/env bash
# Reset to a clean slate between runs:
#   1. delete the local state files (state.json / state.lock)
#   2. tear down the Azure resource group
#
# Run this between steps, or any time a run left things half-built.
# Pass --no-wait to background the cloud delete (default waits until it's gone).
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Removing local state files..."
rm -f "$HERE"/state.json "$HERE"/state.lock
rm -f "$HERE"/src/*/state.json "$HERE"/src/*/state.lock

"$HERE/teardown.sh" "$@"
