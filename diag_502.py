import paramiko
import sys

HOSTNAME = '172.20.7.172'
PORT = 21712
SSH_USER = 'ajbasa'
SSH_PASS = r'H[r=hm5CtQbp{SvzA'

def diagnose():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOSTNAME, port=PORT, username=SSH_USER, password=SSH_PASS, timeout=20)
    
    cmd = """
echo 'H[r=hm5CtQbp{SvzA' | sudo -S bash -c "
echo '=== GUNICORN JOURNAL LOGS ==='
journalctl -u ovpa_website -n 25 --no-pager
echo '=== NGINX ERROR LOG ==='
tail -n 15 /var/log/nginx/error.log
echo '=== SOCKET CHECK ==='
ls -la /run/gunicorn* || true
"
"""
    stdin, stdout, stderr = client.exec_command(cmd)
    raw = stdout.read()
    sys.stdout.buffer.write(raw)
    sys.stdout.flush()
    client.close()

if __name__ == '__main__':
    diagnose()
