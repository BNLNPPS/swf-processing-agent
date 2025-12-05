# Processing Simulator (agent)

---

### About

The processing agent gets notification via MQ, from the data agent,
and initiates interaction with the PanDA system, submitting a task to process
files beloning to a dataset produced during a specific run.

### Static Test

If an input dataset is specified on the commans line, the driver will activate
the static test mode i.e. just test PanDA task submission for that specific dataset.
The purpose is to facilitate debugging, access etc.



