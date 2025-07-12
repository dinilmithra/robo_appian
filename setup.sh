#!/bin/bash

# Exit on any error
set -e

echo "======================================"
echo "  Setting up robo_appian development  "
echo "======================================"
echo ""

# Run setup scripts
echo "Step 1: Setting up environment..."
./scripts/setup-env.sh
echo ""

echo "Step 2: Installing packages..."
./scripts/install-packages.sh
echo ""

echo "Activating environment..."
source ./.venv/bin/activate

echo "======================================"
echo "  Setup completed successfully! 🎉   "
echo "======================================"
echo ""
echo "Next steps:"
# echo "1. Activate the virtual environment: source ./.venv/bin/activate"
echo "2. Start developing: poetry run python -m robo_appian"
echo "3. Build docs: poetry run mkdocs serve"
echo "4. Run tests: poetry run pytest (after setting up tests)"
echo ""