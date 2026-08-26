import paramiko
import sys

HOSTNAME = '172.20.7.172'
PORT = 21712
SSH_USER = 'ajbasa'
SSH_PASS = r'H[r=hm5CtQbp{SvzA'

def see_django_err():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOSTNAME, port=PORT, username=SSH_USER, password=SSH_PASS, timeout=20)
    
    cmd = """
echo '=== DJANGO LOG ==='
tail -n 30 /var/www/ovpa_website/logs/django.log || true
echo '=== JOURNALCTL ==='
journalctl -u ovpa_website -n 25 --no-pager
"""
    stdin, stdout, stderr = client.exec_command(f"echo '{SSH_PASS}' | sudo -S bash -c \"{cmd}\"")
    sys.stdout.buffer.write(stdout.read())
    sys.stdout.flush()
    client.close()

if __name__ == '__main__':
    see_django_err()
