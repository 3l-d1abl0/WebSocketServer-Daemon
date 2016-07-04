
#!/usr/bin/python
import subprocess
import time
import os
import signal

FILE_PATH = "/home/ubuntu/background/Demo/server.php"
FILE = "server.php"

def screen_present(name):
        var = subprocess.check_output(["screen -ls; true"],shell=True)
        if "."+name+"\t(" in var:
                print name+" is running"
        else:
                print name+" is not running"

def spawn():
    '''
    command = 'screen -dmS websocketserver php %s'%(FILE_PATH)
    print ('Command :: ',command)
    p = subprocess.Popen(['screen', '-d', '-m', '-S', 'websocketserver', 'php', FILE_PATH], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = p.communicate(b"input data that is passed to subprocess' stdin")
    
    print (err)
    print (output)
    '''
    
    command = "screen -dmS websocketserver php {}".format(FILE)
    print ('Command: ', command)
    process = subprocess.Popen(command, shell=True,  stdout=subprocess.PIPE)
    #Gives bytes, which is a binary sequence of bytes rather than a string of Unicode characters
    op = process.communicate()[0]
    #wait for Exitcoede
    exit_code = process.wait()
    print ('Exit COde : ',exit_code)
    #Close the Pipe
    process.stdout.close()
    
    decoded_string = op.decode('ascii')
    print('Decoded String : ', decoded_string)

if __name__ == "__main__":
    print ('--MAIN--')
    spawn()
    screen_present("websocketserver")
