#!/usr/bin/python

import subprocess
from websocket import create_connection
import threading
import time
import json
import os

#WebSocket Server Url to Connect
WEBSOCKET_URL = "ws://localhost:8080/serverPush"
#Server File Name
SERVER_FILE =   "server.php"
#WebSocket Connection Object
WS = False

##Checks for the existance of a Unix PID
def check_pid(pid):
    try:
        os.kill(pid, 0)
    except OSError as ex:
        ##LOGGER
        template = "An exception of type {0} occured.\nArguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print (message)
        ##LOGGER
        return False
    else:
        return True
    
    
def checkWebsocketServer():
    global WS
    #LOG Connect to Server
    print('%s : Attempting to Connect to Server .... \n' % ( time.ctime(time.time()) ))
    try:
        WS = create_connection(WEBSOCKET_URL)
        print('%s : Successfully Connected to Server !\n'%(time.ctime(time.time())))
        
        if(type(WS).__name__ is 'WebSocket'):
            print('%s : CLosing WebSocket Server Connection ... \n'%(time.ctime(time.time())))
            WS.close()
            
    except Exception as ex:
        #LOG could NOT connect to server
        #LOG ex.args and TIME
        print('%s : Could not Connect to Server ... \n'%(time.ctime(time.time())))
        template = "An exception of type {0} occured.\nArguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print (message)
        
        #LOG Check if Server is Running and Not Responding !
        #if Running Kill it and Spawn New Server
        #else just Spawn new  Server
        
        #Checking if the Server is Running or Not
        command = "ps aux | grep \"{}\" | grep -v  \"/bin/sh\" | grep -v \"grep\" | head -1 | awk '{{ print $2 }}' ".format(SERVER_FILE)
        print ('Command: ', command)
        process = subprocess.Popen(command, shell=True,  stdout=subprocess.PIPE)
        #Gives bytes, which is a binary sequence of bytes rather than a string of Unicode characters
        op = process.communicate()[0]
        #Close the Pipe
        process.stdout.close()
        
        print ('Returned : ', str(op))
        #Decode to ASCII ## EXCEPTION if its HEX or any other Format
        pid = op.decode('ascii').strip()
        print('Decoded String (PID): ',pid)
        
        #Check if we have a PID for the WebSocket Server 
        if pid and pid.isdigit():
            #Got a PID
            print ("Not Empty and isDigit :: GOT PID")
            ##NOW Kill the existing Running Server
            os.kill(int(pid), signal.SIGTERM)
            
            if check_pid(pid) is True :
                print ('Process is Still Running')
                ##LOGGER 
                ##Failed
                ##??
            else:
                print ('No Process With pid %s '% (pid))
                
        else:
            #NO PID Exists # There is no Server Running
            print ("Empty :: NO Server Running")
            
        ##Start the WebSocket Server
        ##At this point either there is NO WebSocekt Server Runnning or
        ##the Exisitng WebSocket Server (process) has been Killed 
        
        
        
    print ('--Function Ends--')


if __name__ == "__main__":
    print ('--MAIN--')
    checkWebsocketServer()