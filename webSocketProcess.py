#!/usr/bin/python

import subprocess
from websocket import create_connection
import threading
import signal
import time
import json
import sys
import os

#WebSocket Server Url to Connect
_WEBSOCKET_URL = "ws://localhost:8080/serverPush"
#Screen Session Name For Server
_SCREEN_NAME ="websocketserver"
#Server File Name
_SERVER_FILE =   "server.php"
#WebSocket Connection Object
_WS = False


##Makes a Connection to WebSocketServer to check if gets Response
def ping_websocketserver():
    #LOG Connecting to Server
    print('%s : Attempting to Connect to Server ....' % ( time.ctime(time.time()) ))
    try:
        _WS = create_connection(_WEBSOCKET_URL)
        print('%s : Successfully Connected to Server !'%(time.ctime(time.time())))
        #LOG Connected to Server
        if(type(_WS).__name__ is 'WebSocket'):
            print('%s : CLosing WebSocket Server Connection ... '%(time.ctime(time.time())))
            #LOG Connection Closed to Server
            _WS.close()
        #Connected to Server
        return True
            
    except Exception as ex:
        #LOG could NOT connect to server
        #LOG ex.args and TIME
        print('%s : Could not Connect to Server ... '%(time.ctime(time.time())))
        template = "An exception of type {0} occured.\nArguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print (message)
        return False
    

#checks if there is a process running for the WebSocketServer
def check_websocketserver():
    #Checking if the Server is Running or Not
    command = "ps aux | grep \"{}\" | grep -v  \"/bin/sh\" | grep -v \"grep\" | head -1 | awk '{{ print $2 }}' ".format(_SERVER_FILE)
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
        print ('Pid No Empty and Digits : ', pid)
        return pid
    else:
        #NO PID Exists # There is no Server Running
        print ("Empty :: NO Server Running")
        return False


##Tries to Start a WebSocketServer via Screen Session
def spawn():
    #Form the proper Command
    command = "screen -dmS websocketserver php {}".format(_SERVER_FILE)
    print ('Command: ', command)
    
    process = subprocess.Popen(command, shell=True,  stdout=subprocess.PIPE)
    #Gives bytes, which is a binary sequence of bytes rather than a string of Unicode characters
    #op = process.communicate()[0]
    #wait for Exitcoede
    exit_code = process.wait()
    #Close the Pipe
    process.stdout.close()
    #decoded_string = op.decode('ascii')
    #print('Decoded String : ', decoded_string)
    
    if exit_code <0:
        print ('Error while Executing Command : EXIT_STATUS %s'%(exit_code))
        return False
    else:
        print ('Server Started ...')
        return True
    
##Checks if there is Screen Session running for WebSocketServet and tries to Connect it
def new_server_check():
        var = subprocess.check_output(["screen -ls; true"],shell=True)
        if "."+_SCREEN_NAME+"\t(" in var.decode('ascii'):
            #return True
            print('Screen Session is Running')
            return ping_websocketserver()
        
        else:
            #No Screen Started for Server
            return False

        

if __name__ == "__main__":
    while True:
        
        print ('--MAIN--')
        #Ping the WebSoket Server
        ping_result = ping_websocketserver()
        #Testing Setting ping_result to False
        ping_result = False
        #If Cannot Connect to WebSocketServer
        if ping_result is False :
            to_spawn = True
            #Check if Process (Server) is Running
            print ('Checking is Server Process is running !')
            pid = check_websocketserver()
            print ('OP :PID : ',pid)       

            #IF PID not False then its Valid
            if pid: 
                print('PID :',pid)
                print('Killing the existing process with PId : ',pid )
                #Server is Running
                #NOW Kill the existing Running Server
                os.kill(int(pid), signal.SIGTERM)   #os.kill(int(pid), 9)
                print ('Checking if the Process is still Running ... ')           
                time.sleep(5)
                #Check if the Server was Successfully Killed
                process_path = "/proc/{}".format(pid)
                if os.path.exists(process_path):
                    to_spawn = False
                    print('Could not kill Process with PID %s'%(pid))
                    print('Error --')
                    ##LOGGER##FAILED
                    ##BreakLoop??#NoSpawn##
                else:
                    to_spawn = True
                    print('SuccessFully Killed ! No process with PID Exist')


            #Check if new Server Should Spawn
            if not to_spawn:
                print('ERROR :: Failed to Kill Existing Websocket Server !')
                ##LOGGER##FAILED

            else:
                #Spawn a New Server
                print ('Spawning A NEw Server !')
                #print('Breaking....')
                #sys.exit(0)
                spawn_result = spawn()    

                if spawn_result:
                    print('Command to Spawn WebSocketServer ran Successfully')
                    print('Wait for Server to initalize, before checking !')
                    time.sleep(15)
                    print('Checking if Server is Running ... ')

                    #Check is Server is actually running
                    if new_server_check():
                        #Server is Up and Running
                        print('%s : Server is Up and Runnig ... \n' % ( time.ctime(time.time()) ))
                    else:
                        print('%s : ERROR Failed to Start a NewServer ... \n' % ( time.ctime(time.time()) ))
                        ##LOGGER##FAILED
                else:
                    print ('COMMAND FAILED ! Could not start new Server Instance !')
                    ##LOGGER##FAILED


        else:   #ping_result is True
            print ('WebSocketServer is Up and Running & Listening to Connections ! ')

        print ('--MAIN ENDS--')
        time.sleep(10)
