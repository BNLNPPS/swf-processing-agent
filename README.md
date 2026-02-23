# swf-processing-agent

This is the prompt processing agent within the ePIC streaming workflow testbed.
Its function is to manage creation and PanDA tasks for each dataset created by the
_data-agent_.


## PanDA notes

For the --vo option, please use "wlcg".

To submit jobs to BNL PanDA, it's necessary to have a valid OIDC token issued by IAM.

## Startup guide

```
Users submit jobs to PanDA using panda-client tools. More documentation can be found here : https://panda-wms.readthedocs.io/en/latest/client/panda-client.html
Below is a quick example of installing panda-client. 

Create a venv
python3 -m venv pclient
. pclient/bin/activate
pip install panda-client
Config file 
mkdir -p pclient/run
cd pclient/run/
create a setup file in the run directory :
$> cat setup.sh (* example use the EIC VO/group) 
source  <pathname to your “pclient” directory>/etc/panda/panda_setup.sh
export PANDA_URL_SSL=https://pandaserver01.sdcc.bnl.gov:25443/server/panda
export PANDA_URL=https://pandaserver01.sdcc.bnl.gov:25443/server/panda
export PANDACACHE_URL=https://pandaserver01.sdcc.bnl.gov:25443/server/panda
export PANDAMON_URL=https://pandamon01.sdcc.bnl.gov
export PANDA_AUTH=oidc
export PANDA_AUTH_VO=EIC
export PANDA_USE_NATIVE_HTTPLIB=1
export PANDA_BEHIND_REAL_LB=1
```

## Start the agent

### Start individually in CLI mode

```
cd swf-processing-agent
./simulator/processing_simulator.py
```

The agent is started and subscribed to ActiveMQ /topic/epictopic. When a message of type `stf_ready` is broadcasted, the agent will submit the task to PanDA

### Workflow orchestrator

Both this agent and swf-data-agent can be started by the orchestror for prompt processing workflows. 

```
testbed run stf_processing
```

The agents need to be added to the supervisord configuration file `agents.supervisord.conf`

```
[program:stf-data-agent]
command=python %(ENV_SWF_HOME)s/swf-data-agent/simulator/data_simulator.py -v
directory=%(ENV_SWF_HOME)s/swf-testbed
environment=SWF_TESTBED_CONFIG="%(ENV_SWF_TESTBED_CONFIG)s"
autostart=false
autorestart=true
stopwaitsecs=10
stopsignal=QUIT
stdout_logfile=%(here)s/logs/%(program_name)s.log
stderr_logfile=%(here)s/logs/%(program_name)s.log

[program:stf-processing-agent]
command=python -u %(ENV_SWF_HOME)s/swf-processing-agent/simulator/processing_simulator.py
directory=%(ENV_SWF_HOME)s/swf-testbed
environment=SWF_TESTBED_CONFIG="%(ENV_SWF_TESTBED_CONFIG)s"
autostart=false
autorestart=true
stopwaitsecs=10
stopsignal=QUIT
stdout_logfile=%(here)s/logs/%(program_name)s.log
stderr_logfile=%(here)s/logs/%(program_name)s.log
```

Configure the workflow in `stf_processing_default.toml`, an example:

```
[testbed]
namespace = "test-zy"

[workflow]
name = "stf_processing"
version = "1.0"
description = "STF datataking workflow for standard processing"
includes = ["daq_state_machine.toml"]
config = "stf_processing_default"

# =============================================================================
# Agent Configuration
# =============================================================================
# Fast processing requires: data agent, fastmon agent, fast_processing agent
# DAQ simulator runs as the workflow runner (always present)

[agents.stf-data]
enabled = true
script = "../swf-data-agent/simulator/data_simulator.py"

[agents.stf-processing]
enabled = true
script = "../swf-processing-agent/simulator/processing_simulator.py"

[stf_processing]
# Count-based STF generation
stf_count = 2                   # Generate exactly 10 STF files
physics_period_count = 1        # Single physics period
```
