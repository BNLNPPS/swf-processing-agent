"""
Tests for the swf_processing_agent main module.
"""

import pytest
import sys

def test_main_module_imports():
    """Test that the main module can be imported."""
    import swf_processing_agent.main
    assert hasattr(swf_processing_agent.main, 'main')

def test_package_version():
    """Test that the package has a version."""
    import swf_processing_agent
    assert hasattr(swf_processing_agent, '__version__')
    assert swf_processing_agent.__version__ == "0.1.0"