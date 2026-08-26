import paramiko
import sys

HOSTNAME = '172.20.7.172'
PORT = 21712
SSH_USER = 'ajbasa'
SSH_PASS = r'H[r=hm5CtQbp{SvzA'

def fix():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOSTNAME, port=PORT, username=SSH_USER, password=SSH_PASS, timeout=20)
    
    script = """
set -e
cd /var/www/ovpa_website
git reset --hard origin/master
git pull origin master
source venv/bin/activate
python manage.py collectstatic --noinput --clear
systemctl restart ovpa_website
systemctl restart nginx

sleep 2
echo "=== HTTP STATUS TEST ==="
curl -s -I http://127.0.0.1/
"""
    cmd = f"echo '{SSH_PASS}' | sudo -S bash -c \"{script}\""
    stdin, stdout, stderr = client.exec_command(cmd)
    sys.stdout.buffer.write(stdout.read())
    sys.stdout.buffer.write(stderr.read())
    sys.stdout.flush()
    client.close()

if __name__ == '__main__':
    fix()
