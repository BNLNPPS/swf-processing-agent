# DAQ Simulation & PanDA Submission Script

This script runs a DAQ simulation, optionally sends and receives messages over MQ, and optionally submits jobs to the PanDA when STF messages are received.

## Overview

The script is designed to:
- Simulate the generation of STF based on a configurable schedule.
- Send STF messages to an MQ server.
- Listen for STF messages from MQ, and optionally submit corresponding jobs to PanDA.

It integrates with:
- daq package: for DAQ simulation.
- comms package: for MQ sender/receiver.
- pandaclient package: for PanDA job submission.

---

## Usage

python3 run_daqsim.py [options]


### Available options:
| Option | Description | Default |
|--------|-------------|---------|
| `-v`, `--verbose` | Enable verbose/debug output | `False` |
| `-m`, `--mq` | Enable MQ send/receive | `False` |
| `--submit-panda` | Submit STF jobs to PanDA when receiving MQ messages | `False` |
| `-s`, `--schedule` | Path to schedule YAML file | `$DAQSIM_PATH/config/schedule-rt.yml` |
| `-d`, `--dest` | Output folder for generated STFs | `''` |
| `-f`, `--factor` | Time scaling factor for simulation | `1.0` |
| `-u`, `--until` | Stop simulation after this many seconds | `None` |
| `-c`, `--clock` | Simulation clock frequency (seconds) | `1.0` |
| `-L`, `--low` | Low STF production time limit | `1.0` |
| `-H`, `--high` | High STF production time limit | `2.0` |

---

## Examples

### Run DAQ simulation (generate STF events):
python3 run_daqsim.py -v

### Run with MQ sender/receiver:
python3 run_daqsim.py -v -m

### Run with MQ and submit jobs to PanDA:
python3 run_daqsim.py -v -m --submit-panda

---

## Output

The script prints:
- Start and end times of the DAQ simulation.
- Number of STFs generated.
- If MQ is enabled: connection and message logs.
- If PanDA submission is enabled: job submission status, JEDI Task IDs, and monitoring URLs.
