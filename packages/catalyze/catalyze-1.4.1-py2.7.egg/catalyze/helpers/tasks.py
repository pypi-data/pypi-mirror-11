from __future__ import absolute_import

import sys, time
from catalyze import config, output

def poll_status(session, env_id, task_id, exit_on_error=True):
    route = "%s/v1/environments/%s/tasks/%s" % (config.paas_host, env_id, task_id)
    while True:
        time.sleep(2)
        task = session.get(route, verify = True)
        if task["status"] not in ["scheduled", "queued", "started", "running"]:
            if task["status"] == "finished":
                return task
            else:
                output.write("")
                output.error("Error - ended in status '%s'." % (task["status"],), exit=exit_on_error)
        else:
            output.write(".", sameline = True)
