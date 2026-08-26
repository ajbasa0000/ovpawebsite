import paramiko

HOSTNAME = '172.20.7.172'
PORT = 21712
SSH_USER = 'ajbasa'
SSH_PASS = r'H[r=hm5CtQbp{SvzA'

def query():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOSTNAME, port=PORT, username=SSH_USER, password=SSH_PASS, timeout=20)
    
    sftp = client.open_sftp()
    py_code = """
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ovpa_website.settings')
django.setup()
from cms.models import Issuance, NewsArticle, Event, Service, Project

print("=== DATABASE RECORD COUNTS ===")
print("Issuances:", Issuance.objects.count())
print("News Articles:", NewsArticle.objects.count())
print("Events:", Event.objects.count())
print("Services:", Service.objects.count())
print("Projects:", Project.objects.count())

print("\n=== LATEST ISSUANCES ===")
for i in Issuance.objects.all()[:5]:
    print(f"- [{i.issuance_number}] {i.title} (status: {i.status}, date: {i.issuance_date})")
"""
    with sftp.file('/tmp/check_counts.py', 'w') as f:
        f.write(py_code)
    sftp.close()
    
    stdin, stdout, stderr = client.exec_command("/var/www/ovpa_website/venv/bin/python /tmp/check_counts.py")
    print(stdout.read().decode('utf-8', errors='ignore'))
    client.close()

if __name__ == '__main__':
    query()
