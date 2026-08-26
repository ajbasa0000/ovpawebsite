import paramiko
import sys

HOSTNAME = '172.20.7.172'
PORT = 21712
SSH_USER = 'ajbasa'
SSH_PASS = r'H[r=hm5CtQbp{SvzA'

def insert_issuances_sftp():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOSTNAME, port=PORT, username=SSH_USER, password=SSH_PASS, timeout=20)
    
    sftp = client.open_sftp()
    
    script_content = """import os, django, datetime
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ovpa_website.settings')
django.setup()

from cms.models import Issuance, Document
from django.contrib.auth import get_user_model

User = get_user_model()
admin_user = User.objects.filter(is_superuser=True).first()

issuances = [
    ('MEMO-2026-001', 'Revised Guidelines on Administrative Staff Development Program', 'memo', '2026-03-01'),
    ('MEMO-2026-002', 'Call for Nominations: Outstanding Administrative Personnel 2026', 'memo', '2026-03-05'),
    ('CIRCULAR-2026-01', 'Institutional Policy on Digital Transformation for Office Operations', 'circular', '2026-02-25'),
    ('ORDER-2026-04', 'Implementation of Synchronized Performance Review Cycle', 'order', '2026-03-10'),
    ('RES-2026-08', 'Resolution on the Adoption of Sustainable Campus Management Practices', 'resolution', '2026-02-11'),
]

for num, title, itype, dstr in issuances:
    obj, created = Issuance.objects.update_or_create(
        issuance_number=num,
        defaults={
            'title': title,
            'issuance_type': itype,
            'issuance_date': datetime.datetime.strptime(dstr, '%Y-%m-%d').date(),
            'content': title + ' - Official directive issued by the Office of the Vice President for Administration, UP System.',
            'status': 'published',
            'created_by': admin_user
        }
    )
    print(f"Saved Issuance: {obj.issuance_number} | Created: {created}")

print(f"Total Database Issuances: {Issuance.objects.count()}")
"""
    with sftp.file('/tmp/insert_issuances.py', 'w') as f:
        f.write(script_content)
    sftp.close()
    
    cmd = "/var/www/ovpa_website/venv/bin/python /tmp/insert_issuances.py"
    stdin, stdout, stderr = client.exec_command(f"echo '{SSH_PASS}' | sudo -S bash -c \"{cmd}\"")
    sys.stdout.buffer.write(stdout.read())
    sys.stdout.buffer.write(stderr.read())
    sys.stdout.flush()
    client.close()

if __name__ == '__main__':
    insert_issuances_sftp()
