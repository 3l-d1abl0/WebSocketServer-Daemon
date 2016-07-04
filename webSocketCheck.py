#!/usr/bin/python
from websocket import create_connection
import threading
#import thread
import time
import json

#WebSocket Server to Connect
#server ="ws://localhost:8080/serverPush"
#WebSocket Connection Object
WS = False

def spawn_socket(no_mess):
    global WS
    #LOG Connect to Server 
    print("%s : Attempting to Connect to Server .... : \n" % ( time.ctime(time.time()) ))
    try:
        WS = create_connection(server)
        print("%s : Successfully Connected to Server !\n"%(time.ctime(time.time())))
    except Exception as ex:
        #LOG could NOT connect to server
        #LOG ex.args and TIME
        print("%s Could not Connect to Server ... \n !"%(time.ctime(time.time())))
        
        #LOG Check if Server is Running
        #if Running Kill it and Spawn New Server
        #else just Spawn new  Server
        
    if(type(WS).__name__ is 'WebSocket'):
        print("%s : CLosing WebSocket Server Connection ... \n"%(time.ctime(time.time())))
        WS.close()


#no_conn = int(raw_input("No of connections ?? "))
no_mess = int(input("No. of Messages ?? "))

spawn_socket(no_mess)

print("%s : --- Exiting Main Thread ---" % (time.ctime(time.time())))


'''

WebSocket   bool

An exception of type error occured. Arguments:
(10054, 'An existing connection was forcibly closed by the remote host')

Connection Error !
An exception of type error occured. Arguments:
(10061, 'No connection could be made because the target machine actively refused it')

'''
