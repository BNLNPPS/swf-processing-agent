# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Testing
- `./run_tests.sh` - Run tests with proper environment setup
- Tests use pytest framework  
- Test runner manages virtual environment automatically

### Agent Management
- `python stf_processing/run_daqsim.py` - Run DAQ simulation and PanDA job submission
- `python stf_processing/mq_receiver_panda_submission.py` - Message queue receiver for PanDA jobs
- Agent processes managed by supervisord when run as part of full testbed

### Installation and Dependencies
**CRITICAL: Run install.sh from swf-testbed directory to set up environment**
- Dependencies in `pyproject.toml` (installed by testbed install.sh)
- Virtual environment managed by swf-testbed at `$PARENT_DIR/swf-testbed/.venv/`
- PARENT_DIR environment variable set by install.sh for proper coordination

## Architecture Overview

### PanDA Processing Agent
This is a standalone agent component of the SWF testbed system. It provides:
- PanDA job configuration and submission for streaming workflows
- Integration with message queue system for workflow coordination
- DAQ simulation for STF (Super Time Frame) data generation
- Processing pipeline coordination with other testbed agents

### Key Components
- **DAQ Simulation**: Generates STF events based on configurable schedules
- **PanDA Integration**: Job submission and monitoring via PanDA workload management system
- **Message Queue Processing**: ActiveMQ integration for workflow coordination
- **STF Processing**: Handles processing requests for ePIC detector data

### Multi-Repository Integration
- **swf-testbed**: Orchestrates this agent via supervisord
- **swf-common-lib**: Uses shared utilities for logging and common functionality
- **swf-monitor**: Reports status and metrics to monitoring system
- Part of coordinated multi-repository development workflow

## Configuration and Environment

### PanDA Configuration
- PanDA server connection configuration via environment variables
- Job submission templates and workflow definitions
- Processing queue and resource management settings

### Message Queue Integration
- ActiveMQ connection via environment variables inherited from testbed
- Message processing for STF file notifications and workflow triggers
- Error handling and retry logic for failed processing jobs

### Agent Configuration
- Schedule files for DAQ simulation timing
- Output destination configuration for generated STFs
- Time scaling factors and simulation parameters

## Development Practices

### Multi-Repository Coordination
- Always use infrastructure branches: `infra/baseline-v1`, `infra/baseline-v2`, etc.
- Coordinate changes with sibling repositories (swf-testbed, swf-monitor, swf-common-lib)
- Never push directly to main - always use branches and pull requests
- Run tests across all repositories with `../swf-testbed/run_all_tests.sh`

### Agent Development Patterns
- Async message processing patterns
- PanDA API integration best practices
- Error handling and logging standards using swf-common-lib
- Resource management and cleanup for long-running processes

### Testing Strategy
- Unit tests for PanDA integration components
- Mock external dependencies (PanDA, ActiveMQ, external APIs)
- Integration tests for DAQ simulation workflows
- End-to-end testing with message queue integration

## Branching and PR Guidelines

- Use feature branches for new development (e.g., feature/your-feature-name).
- Open pull requests against the main branch for review.
- Ensure all tests pass before merging.
- Keep infrastructure and environment setup consistent with other SWF repos.

## Key Files and Directories

### Core Processing Files
- `stf_processing/run_daqsim.py` - Main DAQ simulation and PanDA submission script
- `stf_processing/mq_receiver_panda_submission.py` - Message queue receiver
- `stf_processing/my_script.sh` - Supporting shell scripts

### Configuration
- `pyproject.toml` - Package configuration and dependencies
- `pytest.ini` - Test configuration
- `run_tests.sh` - Test execution script

### Testing
- `tests/` - Test suite for agent functionality
- `tests/conftest.py` - Pytest configuration and fixtures

## External Dependencies

### Core Technologies
- **PanDA**: Distributed workload management system for job execution
- **ActiveMQ**: Message broker integration for workflow coordination
- **swf-common-lib**: Shared utilities (logging, etc.)

### Python Dependencies
- Standard libraries for agent functionality
- Message queue client libraries
- PanDA client libraries (when available)
- Testing frameworks (pytest)

## Service Integration

### Supervisor Configuration
When run as part of the full testbed, this agent runs as supervised processes configured in swf-testbed:
- `swf-processing-agent` - Main processing daemon
- Configured via supervisord.conf in swf-testbed

### Workflow Integration
- Receives STF file notifications via message queue
- Submits processing jobs to PanDA for workflow execution
- Reports status and metrics to swf-monitor
- Coordinates with other agents (swf-data-agent, swf-fastmon-agent)

### Security Considerations
- PanDA credentials via environment variables
- Secure handling of job submission parameters
- Resource access control and monitoring
- Message queue authentication via testbed configuration