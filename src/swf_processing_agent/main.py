"""
Main entry point for the SWF Processing Agent.

This module provides the command-line interface for the processing agent,
integrating DAQ simulation and PanDA job submission functionality.
"""

import sys
import os
from swf_common_lib.logging_utils import setup_logger
import logging

db_params = {}
logger = setup_logger(name="swf-processing-agent", db_params=db_params)
logger.info("SWF Processing Agent started")

# Example: Read PanDA and ActiveMQ config from environment
panda_server = os.getenv("PANDA_SERVER", "localhost")
activemq_host = os.getenv("ACTIVEMQ_HOST", "localhost")
activemq_port = os.getenv("ACTIVEMQ_PORT", "61613")
logger.info(f"PanDA server: {panda_server}, ActiveMQ: {activemq_host}:{activemq_port}")

def main():
    """Main entry point for the swf-processing-agent command."""
    # Add the stf_processing directory to path for legacy script access
    current_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(os.path.dirname(current_dir))
    stf_processing_path = os.path.join(repo_root, "stf_processing")
    sys.path.insert(0, stf_processing_path)
    
    # Import and run the existing run_daqsim script
    try:
        from run_daqsim import main as run_daqsim_main
        run_daqsim_main()
    except ImportError:
        logger.error("Cannot import run_daqsim module")
        logger.error(f"Expected path: {stf_processing_path}")
        sys.exit(1)

if __name__ == "__main__":
    main()