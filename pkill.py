#!/usr/bin/python
import subprocess
import time
import os
import signal

PID = 10128

def check_pid(pid):        
    """ Check For the existence of a unix pid. """
    try:
        os.kill(pid, 0)
    except OSError as ex:
        template = "An exception of type {0} occured.\nArguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print (message)
        return False
    else:
        return True

##NOW Kill the existing Running Server
os.kill(int(PID), signal.SIGTERM)

if check_pid(PID) is True :
    print ('Process is Still Running')
else:
    print ('No Process With pid %s '% (PID))