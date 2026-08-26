import paramiko
import sys

HOSTNAME = '172.20.7.172'
PORT = 21712
SSH_USER = 'ajbasa'
SSH_PASS = r'H[r=hm5CtQbp{SvzA'

def ensure():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOSTNAME, port=PORT, username=SSH_USER, password=SSH_PASS, timeout=20)
    
    sftp = client.open_sftp()
    py_code = """import os, sys, django

sys.path.insert(0, '/var/www/ovpa_website')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ovpa_website.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

groot, created = User.objects.get_or_create(username='grootadmin', defaults={'email': 'ajbasa@up.edu.ph', 'is_staff': True, 'is_superuser': True})
groot.set_password('xiarabasa12')
groot.is_staff = True
groot.is_superuser = True
groot.is_active = True
groot.save()

print("=== ALL SUPERUSERS ON STAGING ===")
for u in User.objects.filter(is_superuser=True):
    print(f"- {u.username} (Email: {u.email})")
"""
    with sftp.file('/var/www/ovpa_website/set_groot.py', 'w') as f:
        f.write(py_code)
    sftp.close()
    
    cmd = "cd /var/www/ovpa_website && /var/www/ovpa_website/venv/bin/python /var/www/ovpa_website/set_groot.py && rm -f /var/www/ovpa_website/set_groot.py"
    stdin, stdout, stderr = client.exec_command(f"echo '{SSH_PASS}' | sudo -S bash -c \"{cmd}\"")
    sys.stdout.buffer.write(stdout.read())
    sys.stdout.flush()
    client.close()

if __name__ == '__main__':
    ensure()
