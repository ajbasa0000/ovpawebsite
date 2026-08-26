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
    
    script = """
set -e
cd /var/www/ovpa_website
source venv/bin/activate
python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ovpa_website.settings')
django.setup()
from django.test import RequestFactory
from ovpa_website.urls import urlpatterns
from django.urls import resolve
from cms.views import home

rf = RequestFactory()
req = rf.get('/', HTTP_HOST='ovpa-dev.up.edu.ph')
try:
    resp = home(req)
    print('Home view executed successfully! Status:', resp.status_code)
except Exception as e:
    import traceback
    traceback.print_exc()
"
"""
    cmd = f"echo '{SSH_PASS}' | sudo -S bash -c \"{script}\""
    stdin, stdout, stderr = client.exec_command(cmd)
    sys.stdout.buffer.write(stdout.read())
    sys.stdout.flush()
    client.close()

if __name__ == '__main__':
    debug_request()
