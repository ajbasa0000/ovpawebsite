import paramiko
import sys

HOSTNAME = '172.20.7.172'
PORT = 21712
SSH_USER = 'ajbasa'
SSH_PASS = r'H[r=hm5CtQbp{SvzA'

def debug_request():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOSTNAME, port=PORT, username=SSH_USER, password=SSH_PASS, timeout=20)
    
    sftp = client.open_sftp()
    py_test = """
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ovpa_website.settings')
django.setup()

from django.test import Client
c = Client()
resp = c.get('/', HTTP_HOST='ovpa-dev.up.edu.ph')
print("CLIENT STATUS CODE:", resp.status_code)
if resp.status_code != 200:
    print("CONTENT:", resp.content.decode('utf-8', errors='ignore')[:500])
"""
    with sftp.file('/tmp/test_client.py', 'w') as f:
        f.write(py_test)
    sftp.close()
    
    cmd = f"echo '{SSH_PASS}' | sudo -S bash -c \"/var/www/ovpa_website/venv/bin/python /tmp/test_client.py\""
    stdin, stdout, stderr = client.exec_command(cmd)
    sys.stdout.buffer.write(stdout.read())
    sys.stdout.buffer.write(stderr.read())
    sys.stdout.flush()
    client.close()

if __name__ == '__main__':
    debug_request()
