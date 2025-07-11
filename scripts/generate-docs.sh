#!/bin/bash

# Robo Appian Documentation Generation Script

echo "🚀 Generating documentation for Robo Appian..."

# Activate virtual environment
source .venv/bin/activate

# Install documentation dependencies
echo "📦 Installing documentation dependencies..."
pip install mkdocs mkdocs-material mkdocstrings[python]

# Build documentation
echo "🔨 Building documentation..."
mkdocs build

# Check if build was successful
if [ $? -eq 0 ]; then
    echo "✅ Documentation built successfully!"
    echo "📁 Documentation files are in the 'site' directory"
    echo ""
    echo "To serve documentation locally:"
    echo "  mkdocs serve"
    echo ""
    echo "To deploy to GitHub Pages:"
    echo "  mkdocs gh-deploy"
    echo ""
else
    echo "❌ Documentation build failed!"
    exit 1
fi
