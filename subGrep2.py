import subprocess

server = "server.php"
#command = "ps aux | grep \"{}\" | grep -v \"/bin/sh\" | head -1 | awk '{{ print $2 }}' ".format(server)
#command = "ps aux | grep \"{}\" |grep -v \"/bin/sh\" |  head -1 ".format(server)
command = "ps aux | grep \"{}\" | grep -v  \"/bin/sh\" | grep -v \"grep\" | head -1 | awk '{{ print $2 }}' ".format(server)

print ('Command: ', command)

process = subprocess.Popen(command, shell=True,  stdout=subprocess.PIPE)

#process.stdout.close()

op = process.communicate()[0]

print ('Returned : ', str(op))

decoded_string = op.decode('ascii')

if decoded_string.strip()and decoded_string.strip().isdigit():
    print ("Not Empty and isDigit")
else:
    print ("Empty")

print('Decoded String : ',decoded_string)

stdout_list =str( op ).split('\n')

print (stdout_list[0])

pid =  stdout_list[0].strip()

print (pid.split('\\n')[0].split('b\''))
