import subprocess
import shlex

proc1 = subprocess.Popen(shlex.split('ps aux'), stdout=subprocess.PIPE)
#Get Server.php
proc2 = subprocess.Popen(shlex.split('grep  "server.php"'), stdin=proc1.stdout, stdout=subprocess.PIPE, stderr = subprocess.PIPE)
#Remove Sel Grep 
proc3= subprocess.Popen(shlex.split('grep -v "grep"'), stdin=proc2.stdout, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
#Get First Process
#proc3 = subprocess.Popen(shlex.split('head -1'), stdin=proc2.stdout, stdout=subprocess.PIPE, stderr =  subprocess.PIPE)

proc1.stdout.close()
proc2.stdout.close()

out, err = proc3.communicate()
#print('out: {0}'.format(out))
#print('err: {0}'.format(err))
#proc2.stdout.close()
#print (proc2.communicate()[0])
#print (out)
new_split = str(out).split('\\n')
i=0
print ('Length :: ',len(new_split))
for x in new_split:
    print (i," :: " ,x)
    i+=1
#print (new_split[0])
proc3.stdout.close()
