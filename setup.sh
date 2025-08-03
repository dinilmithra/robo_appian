#!/bin/bash

# Exit on any error
set -e

echo "======================================"
echo "  Setting up robo_appian development  "
echo "======================================"
echo ""

# Run setup scripts
echo "Step 1: Setting up environment..."
echo "Checking Python version..."
python --version

echo "Creating virtual environment..."
python -m venv ./.venv

echo "Virtual environment created at ./.venv"
echo ""

echo "Activating environment..."
source ./.venv/bin/activate

echo "Upgrading pip..."
python -m pip install --upgrade pip
python -m pip --version

echo "Checking if Poetry is installed..."
if ! command -v poetry &> /dev/null; then
    echo "Poetry not found. Installing from requirements.txt..."
    python -m pip install -r requirements.txt
    echo "Poetry and development tools installed successfully!"
else
    echo "Poetry is already installed. Installing remaining development dependencies..."
    python -m pip install -r requirements.txt
fi

echo "Configuring Poetry to use local virtual environment..."
poetry config virtualenvs.in-project true

echo "Installing project dependencies with Poetry..."
poetry install

echo "Verifying installation..."
poetry show --tree

echo "Package installation completed!"
echo ""

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