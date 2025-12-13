#!/bin/bash
# requirements.txt生成スクリプト
# uv.lockからbase.txtとdev.txtを自動生成する

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
REQUIREMENTS_DIR="$PROJECT_ROOT/requirements"

cd "$PROJECT_ROOT"

echo "Exporting base dependencies..."
uv export --group base -o "$REQUIREMENTS_DIR/base.txt"

echo "Exporting dev dependencies..."
uv export --group dev -o "$REQUIREMENTS_DIR/dev.txt"

echo "Requirements files generated successfully:"
echo "  - $REQUIREMENTS_DIR/base.txt"
echo "  - $REQUIREMENTS_DIR/dev.txt"

