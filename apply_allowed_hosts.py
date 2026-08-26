import paramiko
import sys

HOSTNAME = '172.20.7.172'
PORT = 21712
SSH_USER = 'ajbasa'
SSH_PASS = r'H[r=hm5CtQbp{SvzA'

def deploy():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOSTNAME, port=PORT, username=SSH_USER, password=SSH_PASS, timeout=20)
    
    script = """
set -e
cd /var/www/ovpa_website
git pull origin master

cat << 'ENV' > /var/www/ovpa_website/.env
DEBUG=False
SECRET_KEY=django-insecure-ovpa-staging-prod-key-up-edu-ph-2026
ALLOWED_HOSTS=*
DB_ENGINE=django.db.backends.postgresql
DB_NAME=ovpa_db
DB_USER=ovpa_admin
DB_PASSWORD=9x-ZJ@k&dT$7(gE{4fP_3}r
DB_HOST=127.0.0.1
DB_PORT=5432
ENV

systemctl restart ovpa_website
systemctl restart nginx

sleep 2
echo "=== ALLOWED HOSTS TEST ==="
curl -s -I -H "Host: ovpa-dev.up.edu.ph" http://127.0.0.1/ | head -n 5
"""
    cmd = f"echo '{SSH_PASS}' | sudo -S bash -c \"{script}\""
    stdin, stdout, stderr = client.exec_command(cmd)
    sys.stdout.buffer.write(stdout.read())
    sys.stdout.flush()
    client.close()

if __name__ == '__main__':
    deploy()
