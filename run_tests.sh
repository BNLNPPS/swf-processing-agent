#!/bin/bash

# Test runner for swf-processing-agent
# Follows testbed conventions for environment and execution

echo "Running swf-processing-agent tests..."

# Check for SWF_PARENT_DIR
if [ -z "$SWF_PARENT_DIR" ]; then
    echo "❌ Error: SWF_PARENT_DIR is not set. Please source install.sh in swf-testbed first to set up your environment."
    exit 1
fi

# Check if we're in an active virtual environment or find testbed venv
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "Using active virtual environment: $VIRTUAL_ENV"
elif [[ -f "$SWF_PARENT_DIR/swf-testbed/.venv/bin/activate" ]]; then
    echo "Activating testbed virtual environment from $SWF_PARENT_DIR/swf-testbed/.venv/"
    source "$SWF_PARENT_DIR/swf-testbed/.venv/bin/activate"
else
    echo "Error: No active virtual environment found and cannot locate testbed .venv/"
    echo "Please ensure:"
    echo "1. You have sourced install.sh from swf-testbed directory, OR"
    echo "2. You are in an active virtual environment with required dependencies"
    exit 1
fi

# Verify pytest is available
if ! command -v pytest &> /dev/null; then
    echo "Error: pytest not found in current environment"
    echo "Please install test dependencies: pip install -e .[test]"
    exit 1
fi

# Run tests with coverage
echo "Executing tests..."
pytest -v --cov=src --cov-report=term-missing

echo "swf-processing-agent tests completed successfully!"