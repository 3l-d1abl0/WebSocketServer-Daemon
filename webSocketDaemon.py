#python ./webSocketDaemon.py start
#python ./webSocketDaemon.py stop

#third party libs
from websocket import create_connection
from daemon import runner
#system
import subprocess
import logging
import signal
import time
import json
import sys
import os


#Defaults for the Logger
_LOGGER = False
_HANDLER = False
_LOG_FILE = '/home/ubuntu/background/Demo/webSocketDaemon.log'
#Defaults for the Daemon
_STDOUT_PATH = '/home/ubuntu/background/Demo/daemon/daemon.log'
_STDERR_PATH = '/home/ubuntu/background/Demo/daemon/daemon.log'
_PIDFILE_PATH ='/home/ubuntu/background/Demo/daemon/daemon.pid'
_PIDFILE_TIMEOUT = 3
#WebSocket Server Url to Connect
_WEBSOCKET_URL = "ws://localhost:8080/serverPush"
#Screen Session Name For Server
_SCREEN_NAME ="websocketserver"
#Server File Name
_SERVER_FILE ="server.php"
#Current Working Directory (location of server Name)
_CWD='/'
#WebSocket Connection Object
_WS = False
#Time interval to check server (in seconds)
_INTERVAL = 10
#Set TimeZone for LOf Time
os.environ['TZ'] = 'Asia/Kolkata'


def setup_logger():
    global _LOGGER
    _LOGGER = logging.getLogger('DaemonLog')
    #Set the minimum Log Level
    _LOGGER.setLevel(logging.INFO)
    #Set the FileHandler for Logger
    handler = logging.FileHandler(_LOG_FILE)
    #Set The Logging Format
    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%d-%m-%Y %H:%M:%S  %Z%z'))
    _LOGGER.addHandler(handler)
    
    return handler

def is_daemon_running():
    global _PIDFILE_PATH
    global _PIDFILE_TIMEOUT
    lockfile = runner.make_pidlockfile(_PIDFILE_PATH, _PIDFILE_TIMEOUT)
    if lockfile.is_locked():
        return True
    return False

class Monitor():

    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = _STDOUT_PATH
        self.stderr_path = _STDERR_PATH
        self.pidfile_path = _PIDFILE_PATH
        self.pidfile_timeout = _PIDFILE_TIMEOUT

    ##Makes a Connection to WebSocketServer to check if gets Response
    def ping_websocketserver(self):
        _LOGGER.info('Pinging the Server %s ...'%(_WEBSOCKET_URL))
        try:
            _WS = create_connection(_WEBSOCKET_URL)
            _LOGGER.info('Connected to Server %s ...'%(_WEBSOCKET_URL))
            if(type(_WS).__name__ is 'WebSocket'):
                _LOGGER.info('Closing connection to %s ...'%(_WEBSOCKET_URL))
                #LOG Connection Closed to Server
                _WS.close()
            #Connected to Server
            return True

        except Exception as ex:
            _LOGGER.warn('Could not connect to %s ...'%(_WEBSOCKET_URL))
            template = "An exception of type {0} occured.\nArguments:\n{1!r}"
            _LOGGER.error(template.format(type(ex).__name__, ex.args))
            return False
    
    ##checks if there is a process running for the WebSocketServer
    def check_websocketserver(self):
        _LOGGER.info('Checking for websocket Server Process ...')
        command = "ps aux | grep \"{}\" | grep -v  \"/bin/sh\" | grep -v \"grep\" | head -1 | awk '{{ print $2 }}' ".format(_SERVER_FILE)
        _LOGGER.info('Command: %s'%(command))
        process = subprocess.Popen(command, shell=True,  stdout=subprocess.PIPE)
        op = process.communicate()[0]
        process.stdout.close()
        pid = op.decode('ascii').strip()
        _LOGGER.info('Decoded PID : %s'%(pid))

        #Check if we have a PID for the WebSocket Server 
        if pid and pid.isdigit():
            return pid
        else:
            # There is no Server Running
            _LOGGER.warn('No PID for websocket Server')
            return False

    ##Tries to Start a WebSocketServer via Screen Session
    def spawn(self):
        command = "screen -dmS websocketserver php {}".format(_SERVER_FILE)
        _LOGGER.info('Command : %s'%(command))

        process = subprocess.Popen(command, shell=True, cwd=_CWD, stdout=subprocess.PIPE)
        exit_code = process.wait()
        process.stdout.close()

        if exit_code <0:
            _LOGGER.warn('Error while executing command : EXIT_STATUS : %s'%(exit_code))
            return False
        else:
            _LOGGER.info('command ran successfully ... ')
            return True
    
    
    
    
    ##Checks if there is Screen Session running for WebSocketServet and tries to Connect it
    def new_server_check(self):
        var = subprocess.check_output(["screen -ls; true"],shell=True)
        if "."+_SCREEN_NAME+"\t(" in var.decode('ascii'):
            _LOGGER.info('Screen Session is Running ... ')
            return self.ping_websocketserver()
        
        else:
            _LOGGER.warn('Screen session couldn\'t be started ... ')
            return False

    def run(self):
        while True:
            _LOGGER.info('--MAIN--')
            ping_result = self.ping_websocketserver()
            
            ##Test
            ping_result = False
            
            #If Cannot Connect to WebSocketServer
            if ping_result is False :
                #Flag to check if a new Process should be started
                to_spawn = True
                #Check if Process (Server) is Running
                pid = self.check_websocketserver()
                
                #IF PID not False then its Valid
                if pid: 
                    _LOGGER.info('Killing process with PID : %s'%(pid))
                    os.kill(int(pid), signal.SIGTERM)   #os.kill(int(pid), 9)
                    _LOGGER.info('Checking if PID : %s is still Running ...'%(pid))
                    #Waiting for /proc/pid file to disappear on process termination
                    time.sleep(5)
                    #Check if the Server was Successfully Killed
                    process_path = "/proc/{}".format(pid)
                    if os.path.exists(process_path):
                        to_spawn = False
                        _LOGGER.error('Could not kill Process with PID : %s'%(pid))
                        _LOGGER.critical('Failed to Kill Existing Websocket Server !')
                    else:
                        to_spawn = True
                        _LOGGER.info('Process with PID : %s successfully killed ...'%(pid))
                        
                #Check if new Server Should Spawn
                if not to_spawn:
                    _LOGGER.critical('Cannot Start a new Server Instance ! ')

                else:
                    #Spawn a New Server
                    _LOGGER.info('Starting a new Server Instance ... ')
                    #print('Breaking....')
                    #sys.exit(0)
                    spawn_result = self.spawn()    

                    if spawn_result:
                        _LOGGER.info('Wait for Server to initalize, before checking it ...')
                        time.sleep(15)
                        _LOGGER.info('Checking if Server is Running ...')
                        if self.new_server_check():
                            #Server is Up and Running
                            _LOGGER.info('Server is up & running ...')
                        else:
                            _LOGGER.critical('Failed to start a new server Instance ...')
                    else:
                        _LOGGER.critical('COMMAND FAILED ! Could not start new Server Instance ... ')
                     
            else:
                _LOGGER.info('WebSocketServer is up & running & Listening to Connections ! ')        

            _LOGGER.info('--MAIN ENDS--')
            time.sleep(_INTERVAL)



if __name__ == "__main__":
    
    if(sys.argv[1]=='start'):
        if is_daemon_running():
            print('This Daemon is Already Running ! In case of Doubt check Daemon\'s PID File')
            exit(0)
            
    #Initialize Logger settings
    _HANDLER = setup_logger()
    #Instantialte Daemon Class
    serverMonitor = Monitor()
    #Assigning current working directory path to _CWD GLobal variable 
    _CWD =os.path.abspath(os.path.dirname('__file__'))
    
    try:
        #Start_daemon
        daemon_runner = runner.DaemonRunner(serverMonitor)
        #This ensures that the logger file handle does not get closed during daemonization
        daemon_runner.daemon_context.files_preserve=[_HANDLER.stream]
        daemon_runner.do_action()
    except runner.DaemonRunnerStartFailureError as e:
        print ('Could not START daemon: {0}'.format(str(e)))
    except runner.DaemonRunnerStopFailureError as e:
        print ('Could not STOP daemon: {0}'.format(str(e)))

    
