
#!/usr/bin/python
import subprocess
import time
import os
import signal

_FILE_PATH = "/home/ubuntu/background/Demo/server.php"
_FILE = "server.php"
#The Screen Name for the Websocket Server
_SCREEN_NAME ="websocketserver"
_WS = False
_WEBSOCKET_URL = "ws://localhost:8080/serverPush"
_CWD = '/home/ubuntu/background/Demo/'

#Fix for Python 2
def new_server_check(self):
    command = 'screen -ls'
    process = subprocess.Popen(command, shell=True,  stdout=subprocess.PIPE)
    op = process.communicate()[0]
    #Close the Pipe
    process.stdout.close()
    #check if _SCREEN_NAME is in output
    if "."+_SCREEN_NAME+"\t(" in op.decode('ascii'):
        _LOGGER.info('Screen Session is Running ... ')
        return self.ping_websocketserver()
    else:
        #No Screen Started for Server
        _LOGGER.warn('Screen session couldn\'t be started ... ')
        return False

#Works for Python 3 #check_output not supported in python 2
def server_check(name):
        var = subprocess.check_output(["screen -ls; true"],shell=True)
        if "."+name+"\t(" in var.decode('ascii'):
            #return True
            
            print('%s : Attempting to Connect to Server .... \n' % ( time.ctime(time.time()) ))
            try:
                _WS = create_connection(_WEBSOCKET_URL)
                print('%s : Successfully Connected to Server !\n'%(time.ctime(time.time())))
                
                if(type(_WS).__name__ is 'WebSocket'):
                    print('%s : CLosing WebSocket Server Connection ... \n'%(time.ctime(time.time())))
                    _WS.close()
                
                #Server is Accepting Requests
                return True
            
            except Exception as ex:
                #LOG could NOT connect to server
                #LOG ex.args and TIME
                print('%s : Could not Connect to Server ... \n'%(time.ctime(time.time())))
                template = "An exception of type {0} occured.\nArguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print (message)
                #Server Cannot Be Connected
                return False
        
        else:
            #No Screen Started for Server Available
            return False


def spawn():
    #Form the proper Command
    command = "screen -dmS websocketserver php {0}".format(_FILE)
    
    print ('Command: ', command)
    
    process = subprocess.Popen(command, shell=True,  stdout=subprocess.PIPE)
    #Gives bytes, which is a binary sequence of bytes rather than a string of Unicode characters
    #op = process.communicate()[0]
    
    #wait for Exitcoede
    exit_code = process.wait()
    if exit_code <0:
        print ('Error while Executing Command : EXIT_STATUS %s'%(exit_code))
    else:
        print ('Server Started ...')
    #Close the Pipe
    process.stdout.close()
    #decoded_string = op.decode('ascii')
    #print('Decoded String : ', decoded_string)
    
    
    
if __name__ == "__main__":
    print ('--MAIN--')
    spawn()
    time.sleep(10)
   # server_check("websocketserver")
    
    if server_check(_SCREEN_NAME) is True:
        print ("There is a Websocketserver Screen !")
    else:
        print ("There is no websocketserver Screen Running !")
        
        
