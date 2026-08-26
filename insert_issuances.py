import paramiko
import sys

HOSTNAME = '172.20.7.172'
PORT = 21712
SSH_USER = 'ajbasa'
SSH_PASS = r'H[r=hm5CtQbp{SvzA'

def run():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOSTNAME, port=PORT, username=SSH_USER, password=SSH_PASS, timeout=20)
    
    cmd = """
/var/www/ovpa_website/venv/bin/python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ovpa_website.settings')
django.setup()
import datetime
from cms.models import Issuance
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
    Issuance.objects.update_or_create(
        issuance_number=num,
        defaults={
            'title': title,
            'issuance_type': itype,
            'issuance_date': datetime.datetime.strptime(dstr, '%Y-%m-%d').date(),
            'content': title + ' - Official directive issued by the Office of the Vice President for Administration.',
            'status': 'published',
            'created_by': admin_user
        }
    )

print('TOTAL ISSUANCES AFTER SEED:', Issuance.objects.count())
"
"""
    stdin, stdout, stderr = client.exec_command(f"echo '{SSH_PASS}' | sudo -S bash -c \"{cmd}\"")
    sys.stdout.buffer.write(stdout.read())
    sys.stdout.flush()
    client.close()

if __name__ == '__main__':
    run()
