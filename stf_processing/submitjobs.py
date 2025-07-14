#!/usr/bin/env python3

import os
import ssl
import json
import time
import uuid
import stomp
from pandaclient import PrunScript, panda_api

# === Configuration ===
host = 'pandaserver02.sdcc.bnl.gov'
port = 61612
cafile = '/eic/u/ejikutu/.globus/full-chain.pem'

panda_auth_vo = os.getenv('PANDA_AUTH_VO')
if not panda_auth_vo:
    print("Error: PANDA_AUTH_VO environment variable is not set.")
    print("Please set it, e.g., 'export PANDA_AUTH_VO=wlcg'")
    exit(1)

mq_user = os.getenv('MQ_USER')
mq_passwd = os.getenv('MQ_PASSWD')

# === PanDA submission ===
def submit_stf_job(stf_message):
    filename = stf_message.get("filename", "unknown")
    generated_uuid = str(uuid.uuid4())
    out_ds_name = f"user.eumaka.{filename}.{generated_uuid}"
    task_name = f"stf_{stf_message.get('state', 'unknown')}_{stf_message.get('substate', 'unknown')}_{generated_uuid[:8]}"

    print(f"[INFO] Submitting job for STF: {filename}")
    print(json.dumps(stf_message, indent=2))

    stf_json_str = json.dumps(stf_message)

    prun_args = [
        "--exec", f"./my_script.sh '{stf_json_str}'",
        "--outDS", out_ds_name,
        "--nJobs", "1",
        "--vo", "wlcg",
        "--site", "BNL_PanDA_1",
        "--prodSourceLabel", "test",
        "--workingGroup", panda_auth_vo,
        "--noBuild",
        "--outputs", "myout.txt"
    ]

    params = PrunScript.main(True, prun_args)
    params["taskName"] = task_name

    c = panda_api.get_api()
    status, result_tuple = c.submit_task(params)

    if status == 0:
        jedi_task_id = result_tuple[2]
        panda_monitor_url = os.getenv('PANDAMON_URL', 'https://pandamon01.sdcc.bnl.gov')
        print(f"[✔] Task submitted successfully! JediTaskID: {jedi_task_id}")
        print(f"[→] Monitor: {panda_monitor_url}/task/{jedi_task_id}/")
    else:
        print(f"[✖] Submission failed. Status: {status}, Message: {result_tuple}")


# === STOMP Listener ===
class STFJobListener(stomp.ConnectionListener):
    def on_message(self, frame):
        print(f"[INFO] Received MQ message: {frame.body}")
        try:
            stf_message = json.loads(frame.body)
            submit_stf_job(stf_message)
        except Exception as e:
            print(f"[ERROR] Failed to parse or submit STF job: {e}")


# === Connect to MQ ===
conn = stomp.Connection(
    host_and_ports=[(host, port)],
    vhost=host,
    try_loopback_connect=False,
    heartbeats=(10000, 10000)
)

conn.transport.set_ssl(
    for_hosts=[(host, port)],
    ca_certs=cafile,
    ssl_version=ssl.PROTOCOL_TLS_CLIENT
)

conn.set_listener('', STFJobListener())

client_id = 'stf-panda-client'
subscription_name = 'stf-panda-sub'

conn.connect(
    login=mq_user,
    passcode=mq_passwd,
    wait=True,
    version='1.2',
    headers={'client-id': client_id}
)

conn.subscribe(
    destination='epictopic',
    id='stf-panda-sub-001',
    ack='auto',
    headers={'activemq.subscriptionName': subscription_name}
)

print(f"[INFO] Listening for STF MQ messages as {client_id}.{subscription_name}...")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting gracefully…")
    conn.disconnect()
