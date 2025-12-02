# swf-processing-agent

This is the prompt processing agent within the ePIC streaming workflow testbed.
Its function is to manage creation and PanDA tasks for each dataset created by the
_data-agent_.


## PanDA notes

For the --vo option, please use "wlcg".

## Startup quide

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