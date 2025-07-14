
# DAQ Simulation & PanDA Submission Scripts

This repository contains scripts to simulate DAQ STF message generation, send and receive STF messages over MQ, and submit jobs to PanDA when STF messages are received.
It also includes dedicated MQ listener scripts that listen for STF messages and submit PanDA jobs.

---

## Overview

The scripts are designed to:
- Simulate the generation of STF (Status Transfer Frame) events based on a configurable schedule.
- Send STF messages to an MQ server.
- Listen for STF messages from MQ and optionally submit corresponding jobs to PanDA.

It integrates with:
- `daq` package — for DAQ simulation.
- `comms` package — for MQ sender/receiver.
- `pandaclient` package — for PanDA job submission.

---

## Usage

Run:
python3 run_daqsim.py [options]

Or, run one of the dedicated MQ receiver scripts:
python3 mq_receiver_panda_submission.py [--verbose] [--submit-panda]

or
python3 submitjobs.py

---

### Available options for `run_daqsim.py`:

| Option               | Description                                     | Default                              |
|-----------------------|-------------------------------------------------|--------------------------------------|
| `-v`, `--verbose`     | Enable verbose/debug output                    | `False`                              |
| `-m`, `--mq`          | Enable MQ send/receive                         | `False`                              |
| `--submit-panda`      | Submit STF jobs to PanDA when receiving MQ messages | `False`                        |
| `-s`, `--schedule`    | Path to schedule YAML file                     | `$DAQSIM_PATH/config/schedule-rt.yml` |
| `-d`, `--dest`        | Output folder for generated STFs              | `''`                                 |
| `-f`, `--factor`      | Time scaling factor for simulation            | `1.0`                                |
| `-u`, `--until`       | Stop simulation after this many seconds       | `None`                               |
| `-c`, `--clock`       | Simulation clock frequency (seconds)          | `1.0`                                |
| `-L`, `--low`         | Low STF production time limit                 | `1.0`                                |
| `-H`, `--high`        | High STF production time limit                | `2.0`                                |

---

## Examples

Run DAQ simulation (generate STF events):
python3 run_daqsim.py -v

Run with MQ sender/receiver:
python3 run_daqsim.py -v -m

Run with MQ and submit jobs to PanDA:
python3 run_daqsim.py -v -m --submit-panda

Run MQ receiver with `comms.py` + PanDA job submitter:
python3 mq_receiver_panda_submission.py -v --submit-panda

Run alternate MQ receiver (without `comms.py`) + PanDA job submitter:
python3 submitjobs.py

---

## MQ STF → PanDA Submitter (`submitjobs.py`)

This script is a dedicated listener that connects to the MQ topic and submits PanDA tasks for each STF message received.

### Highlights:
- Uses `stomp.py` directly (does **not use `comms.py`**).
- Maintains the connection actively with heartbeats.
- Listens on topic: `epictopic` with durable subscription.
- Submits jobs using `pandaclient` with:
  - VO: `wlcg`
  - prodSourceLabel: `managed`
  - unique task names and dataset names.

When a message arrives, it logs the STF JSON and submits to PanDA.
On `Ctrl+C`, it disconnects cleanly.

