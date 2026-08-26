import paramiko
import sys

HOSTNAME = '172.20.7.172'
PORT = 21712
SSH_USER = 'ajbasa'
SSH_PASS = r'H[r=hm5CtQbp{SvzA'

def check_superusers():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOSTNAME, port=PORT, username=SSH_USER, password=SSH_PASS, timeout=20)
    
    script = """
/var/www/ovpa_website/venv/bin/python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ovpa_website.settings')
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()

print('=== SUPERUSERS ON STAGING SERVER ===')
for u in User.objects.filter(is_superuser=True):
    print(f'- Username: {u.username} | Email: {u.email} | Active: {u.is_active}')

# Check if grootadmin exists
groot = User.objects.filter(username='grootadmin').first()
if groot:
    print('--> grootadmin exists.')
else:
    print('--> grootadmin does NOT exist on staging yet.')
"
"""
    stdin, stdout, stderr = client.exec_command(script)
    sys.stdout.buffer.write(stdout.read())
    sys.stdout.flush()
    client.close()

if __name__ == '__main__':
    check_superusers()
