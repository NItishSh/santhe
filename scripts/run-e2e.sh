#!/bin/bash

# Exit on error
set -e

echo "🚀 Setting up E2E Test Environment..."

# Create venv if not exists
if [ ! -d "tests/e2e/venv" ]; then
    python3 -m venv tests/e2e/venv
fi

# Activate venv
source tests/e2e/venv/bin/activate

# Install deps
echo "📦 Installing dependencies..."
pip install -r tests/e2e/requirements.txt > /dev/null

# Install playwright browsers (cached)
echo "🌐 Installing Playwright browsers..."
playwright install chromium

# Run tests
echo "🧪 Running Tests..."
pytest tests/e2e -v -s --html=tests/e2e/report.html --self-contained-html

echo "✅ Tests Completed!"
