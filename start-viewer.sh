#!/bin/bash
# FHIR Patient Viewer
#
# Usage:
#   1. Edit viewer/config.js with your FHIR server URL and credentials
#   2. ./start-viewer.sh

set -e

PORT=${1:-3000}
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Free the port if something is already using it
lsof -ti :"$PORT" | xargs kill 2>/dev/null || true

echo ""
echo "  FHIR Patient Viewer"
echo "  Open: http://localhost:${PORT}"
echo "  Stop: Ctrl+C"
echo ""

python3 "$SCRIPT_DIR/proxy.py" "$PORT"
