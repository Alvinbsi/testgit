import paramiko
import subprocess

cred = open("hosts.csv","r")
creds = cred.readlines()
ssh = paramiko.SSHClient()
for i in creds:
    lines = i.strip()
    ls = lines.split(",")
    response = subprocess.Popen(['ping','-c','1',ls[0]],
            stdout = subprocess.PIPE,
            stderr = subprocess.STDOUT)
    stdout, stderr = response.communicate()
    if response.returncode == 0:
        print(ls[0] + " is up")
        print(ls)
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname="%s"%ls[0],username="%s"%ls[1],password="%s"%ls[2])
        for j in i:

            stdin,stdout,stderr = ssh.exec_command("systemctl status sshd")
            opt = stdout.readlines()
            opt = ls[0]  + "".join(opt)
            tmp = open("%s"%ls[0],"w")
            tmp.write(opt)
            tmp.close()
            stdin,stdout,stderr = ssh.exec_command("uname -r")
            opt1 = stdout.readlines()
            opt1 = ls[0]  + "".join(opt1)
            tmp1 = open("%s"%ls[0],"a")
            tmp1.write(opt1)
            tmp1.close()

    else:
        print(ls[0] + " is down")
cred.close()
