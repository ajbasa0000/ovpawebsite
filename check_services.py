import paramiko
import sys

HOSTNAME = '172.20.7.172'
PORT = 21712
SSH_USER = 'ajbasa'
SSH_PASS = r'H[r=hm5CtQbp{SvzA'

def check():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOSTNAME, port=PORT, username=SSH_USER, password=SSH_PASS, timeout=20)
    
    cmd = """
echo 'H[r=hm5CtQbp{SvzA' | sudo -S bash -c "
systemctl is-active ovpa_website
systemctl is-active nginx
curl -I http://127.0.0.1/
"
"""
    stdin, stdout, stderr = client.exec_command(cmd)
    out = stdout.read().decode('ascii', errors='replace')
    print("OUTPUT:\n", out)
    client.close()

if __name__ == '__main__':
    check()
