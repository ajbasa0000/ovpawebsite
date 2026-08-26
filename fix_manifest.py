import paramiko
import sys

HOSTNAME = '172.20.7.172'
PORT = 21712
SSH_USER = 'ajbasa'
SSH_PASS = r'H[r=hm5CtQbp{SvzA'

def fix_whitenoise_and_manifest():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOSTNAME, port=PORT, username=SSH_USER, password=SSH_PASS, timeout=20)
    
    script = """
set -e
# Use CompressedStaticFilesStorage so missing manifest entries don't crash Django with 500 error
sed -i "s/STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'/STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'/" /var/www/ovpa_website/ovpa_website/settings.py

# Fix base.html line 376
sed -i "s|{% static 'media/transparency-seal.jpg' %}|/media/transparency-seal.jpg|g" /var/www/ovpa_website/templates/base.html

cd /var/www/ovpa_website
source venv/bin/activate
python manage.py collectstatic --noinput

systemctl restart ovpa_website

sleep 2
echo "=== HTTP CODE TEST ==="
curl -s -I http://127.0.0.1/ | head -n 1
"""
    cmd = f"echo '{SSH_PASS}' | sudo -S bash -c \"{script}\""
    stdin, stdout, stderr = client.exec_command(cmd)
    sys.stdout.buffer.write(stdout.read())
    sys.stdout.flush()
    client.close()

if __name__ == '__main__':
    fix_whitenoise_and_manifest()
