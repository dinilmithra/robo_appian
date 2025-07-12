
#!/bin/bash

# Exit on any error
set -e

echo "Checking Python version..."
python --version

echo "Creating virtual environment..."
python -m venv ./.venv

echo "Virtual environment created at ./.venv"
echo "Note: Virtual environment activation should be done manually after setup"