import logging
import time

#third party libs
from daemon import runner

class App():

    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        #self.pidfile_path =  '/var/run/testdaemon/testdaemon.pid'
        self.pidfile_path =  '/c/wspace/Experiments/pythonDaemon.pid'
        self.pidfile_timeout = 5

    def run(self):
        while True:
            #Main code goes here ...
            #Note that logger level needs to be set to logging.DEBUG before this shows up in the logs
            logger.debug("Debug message")
            logger.info("Info message")
            
            #captures TraceBack
            #logger.error('Failed to open file', exc_info=True)
            
            logger.warn("Warning message")
            logger.error("Error message")
            time.sleep(10)

app = App()
logger = logging.getLogger("DaemonLog")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
#handler = logging.FileHandler("/var/log/testdaemon/testdaemon.log")
handler = logging.FileHandler("/c/wspace/Experiments/pythonDaemon.log")
handler.setFormatter(formatter)
logger.addHandler(handler)

daemon_runner = runner.DaemonRunner(app)
#This ensures that the logger file handle does not get closed during daemonization
daemon_runner.daemon_context.files_preserve=[handler.stream]
daemon_runner.do_action()

#python ./pythonDaemon.py start