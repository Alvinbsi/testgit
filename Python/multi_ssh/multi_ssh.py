import paramiko
import subprocess
f = open("results.txt","r+")
f.truncate(0)
cred =open("hosts.csv", "r")
creds = cred.readlines()
ssh = paramiko.SSHClient()
for i in creds:
    line = i.strip()
    ls   = line.split(",")
    response = subprocess.Popen(["ping","-c","1",ls[0]],
            stdout = subprocess.PIPE,
            stderr = subprocess.STDOUT)
    stdout,stderr  = response.communicate()
    if response.returncode == 0:
        print(ls[0] + " is up")
        commands = [
                    "pwd",
                    "id",
                    "uname -a",
                    "df -h"
                   ]
        for command in commands:
            print("="*50, command, "="*50)
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname = "%s"%ls[0],username="%s"%ls[1],password="%s"%ls[2])
            stdin,stdout,stderr = ssh.exec_command(command)
            print(stdout.read().decode())
            opt = stdout.readlines()
            opt = "".join(opt)
            #opt = "#### " + ls[3] +" ###" + "\n" + ls[0] + " -> " + "".join(opt) + "****************************************\n"
            tmp = open("results.txt","w")
            tmp.write(opt)
            tmp.close()
    else:
        print(ls[0] + " is down")
cred.close()
