import paramiko
import sys

HOSTNAME = '172.20.7.172'
PORT = 21712
SSH_USER = 'ajbasa'
SSH_PASS = r'H[r=hm5CtQbp{SvzA'

def fix_all():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOSTNAME, port=PORT, username=SSH_USER, password=SSH_PASS, timeout=20)
    
    script = """
set -e
# 1. Create logs directory and fix permissions
mkdir -p /var/www/ovpa_website/logs /var/www/ovpa_website/media
touch /var/www/ovpa_website/logs/django.log
chown -R ajbasa:www-data /var/www/ovpa_website
chmod -R 775 /var/www/ovpa_website
chmod 664 /var/www/ovpa_website/logs/django.log

# 2. Update settings.py SECURE_SSL_REDIRECT on server to False if no HTTPS certificate is installed yet
# so HTTP traffic does not redirect to broken HTTPS
sed -i 's/SECURE_SSL_REDIRECT = True/SECURE_SSL_REDIRECT = False/' /var/www/ovpa_website/ovpa_website/settings.py || true

# 3. Restart gunicorn and nginx
systemctl reset-failed ovpa_website || true
systemctl restart ovpa_website
systemctl restart nginx

sleep 2
echo "=== GUNICORN STATUS ==="
systemctl is-active ovpa_website
echo "=== HTTP GET TEST ==="
curl -I http://127.0.0.1/
"""
    cmd = f"echo '{SSH_PASS}' | sudo -S bash -c \"{script}\""
    stdin, stdout, stderr = client.exec_command(cmd)
    sys.stdout.buffer.write(stdout.read())
    sys.stdout.flush()
    client.close()

if __name__ == '__main__':
    fix_all()
