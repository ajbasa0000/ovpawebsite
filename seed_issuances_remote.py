import paramiko
import sys

HOSTNAME = '172.20.7.172'
PORT = 21712
SSH_USER = 'ajbasa'
SSH_PASS = r'H[r=hm5CtQbp{SvzA'

def run_seed_cms():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOSTNAME, port=PORT, username=SSH_USER, password=SSH_PASS, timeout=20)
    
    script = """
set -e
cd /var/www/ovpa_website
source venv/bin/activate

cat << 'PYSEED' > run_seed_direct.py
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ovpa_website.settings')
django.setup()

import datetime
from django.utils import timezone
from cms.models import Issuance, NewsArticle, Service, Document
from django.contrib.auth import get_user_model

User = get_user_model()
admin_user = User.objects.filter(is_superuser=True).first()

issuances_data = [
    {
        'title': 'Revised Guidelines on Administrative Staff Development Program',
        'number': 'MEMO-2026-001',
        'type': 'memo',
        'date': datetime.date(2026, 3, 1),
        'content': 'This memorandum outlines the updated procedures and eligibility criteria for administrative staff seeking professional development support...'
    },
    {
        'title': 'Call for Nominations: Outstanding Administrative Personnel 2026',
        'number': 'MEMO-2026-002',
        'type': 'memo',
        'date': datetime.date(2026, 3, 5),
        'content': 'We are pleased to announce the call for nominations for the annual Gawad Parangal for administrative staff who have shown exceptional commitment...'
    },
    {
        'title': 'Institutional Policy on Digital Transformation for Office Operations',
        'number': 'CIRCULAR-2026-01',
        'type': 'circular',
        'date': datetime.date(2026, 2, 25),
        'content': 'To streamline service delivery across all Constituent Units, this circular mandates the adoption of unified digital document tracking systems...'
    },
    {
        'title': 'Implementation of Synchronized Performance Review Cycle',
        'number': 'ORDER-2026-04',
        'type': 'order',
        'date': datetime.date(2026, 3, 10),
        'content': 'This order provides the schedule and mandatory requirements for the first quarter performance evaluation for the year 2026...'
    },
    {
        'title': 'Resolution on the Adoption of Sustainable Campus Management Practices',
        'number': 'RES-2026-08',
        'type': 'resolution',
        'date': datetime.date(2026, 2, 11),
        'content': 'The System Administration hereby adopts the unified framework for sustainability, focusing on energy efficiency and waste reduction in all offices...'
    },
]

for data in issuances_data:
    obj, created = Issuance.objects.update_or_create(
        issuance_number=data['number'],
        defaults={
            'title': data['title'],
            'issuance_type': data['type'],
            'issuance_date': data['date'],
            'content': data['content'],
            'status': 'published',
            'created_by': admin_user
        }
    )
    print(f"Issuance: {obj.issuance_number} (Created: {created})")

print(f"Total Issuances now in Database: {Issuance.objects.count()}")
PYSEED

python run_seed_direct.py
systemctl restart ovpa_website
"""
    cmd = f"echo '{SSH_PASS}' | sudo -S bash -c \"{script}\""
    stdin, stdout, stderr = client.exec_command(cmd)
    sys.stdout.buffer.write(stdout.read())
    sys.stdout.flush()
    client.close()

if __name__ == '__main__':
    run_seed_cms()
