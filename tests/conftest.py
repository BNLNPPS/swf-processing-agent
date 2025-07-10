"""
Pytest configuration and fixtures for swf-processing-agent tests.
"""

import pytest
import os
import sys

# Add the src directory to the Python path for testing
test_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(test_dir)
src_dir = os.path.join(repo_root, "src")
sys.path.insert(0, src_dir)

@pytest.fixture
def sample_config():
    """Provide sample configuration for testing."""
    return {
        "verbose": True,
        "mq": False,
        "submit_panda": False,
        "factor": 1.0,
        "clock": 1.0,
        "low": 1.0,
        "high": 2.0,
    }