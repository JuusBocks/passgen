#!/usr/bin/env bash
# Run passgen on macOS (and Linux)
cd "$(dirname "$0")"
. .venv312/bin/activate
exec passgen
