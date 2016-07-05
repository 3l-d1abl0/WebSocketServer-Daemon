#python ./webSocketDaemon.py start

import logging
import time
#third party libs
from daemon import runner

_LOGGER = False
_HANDLER = False
_LOG_FILE = '/home/ubuntu/background/python/testdaemon.log'


def setup_logger():
    global _LOGGER
    _LOGGER = logging.getLogger('DaemonLog')
    #Set the minimum Log Level
    _LOGGER.setLevel(logging.INFO)
    #Set the FileHandler for Logger
    handler = logging.FileHandler(_LOG_FILE)
    #Set The Logging Format
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', '%d-%m-%Y %H:%M:%S'))
    _LOGGER.addHandler(handler)
    
    return handler

class App():

    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/home/ubuntu/background/python/stdout'
        self.stderr_path = '/home/ubuntu/background/python/stderr'
        self.pidfile_path = '/home/ubuntu/background/python/testdaemon.pid'
        self.pidfile_timeout = 5

    def run(self):
        while True:
            #Main code goes here ...
            #Note that logger level needs to be set to logging.DEBUG before this shows up in the logs
            _LOGGER.debug("Debug message")
            _LOGGER.info("Info message")
            
            #captures TraceBack
            #logger.error('Failed to open file', exc_info=True)
            
            _LOGGER.warn("Warning message")
            _LOGGER.error("Error message")
            time.sleep(10)



if __name__ == "__main__":
    
    #Initialize Logger settings
    _HANDLER = setup_logger()
    
    app = App()
    daemon_runner = runner.DaemonRunner(app)
    #This ensures that the logger file handle does not get closed during daemonization
    daemon_runner.daemon_context.files_preserve=[_HANDLER.stream]
    daemon_runner.do_action()
