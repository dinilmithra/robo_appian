
#!/bin/bash

# Exit on any error
set -e

echo "Upgrading pip..."
python -m pip install --upgrade pip
python -m pip --version

echo "Installing build tools..."
python -m pip install setuptools build twine

echo "Installing Poetry (Python package manager)..."
python -m pip install poetry

echo "Configuring Poetry to use local virtual environment..."
poetry config virtualenvs.in-project true

echo "Installing project dependencies with Poetry..."
poetry install

echo "Verifying installation..."
poetry show --tree

echo "Package installation completed!"
echo "Virtual environment is ready for development."
