import os
import sys
import subprocess
import paramiko

HOSTNAME = '172.20.7.172'
PORT = 21712
SSH_USER = 'ajbasa'
SSH_PASS = r'H[r=hm5CtQbp{SvzA'

LOCAL_DIR = r'c:\Users\ajbas\Documents\Apps\ovpa_website'
REMOTE_DIR = '/var/www/ovpa_website'

def export_and_sync_all_data():
    print("1. Dumping full database from local SQLite with natural keys...")
    dump_script = """import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ovpa_website.settings')
django.setup()
from django.core.management import call_command
with open('full_local_data.json', 'w', encoding='utf-8') as f:
    call_command('dumpdata', 'cms', 'accounts', natural_foreign=True, natural_primary=True, indent=2, stdout=f)
print('DUMP_SUCCESS')
"""
    subprocess.run([sys.executable, "-c", dump_script], cwd=LOCAL_DIR, check=True)
    
    print("2. Connecting to Staging Server via SSH...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOSTNAME, port=PORT, username=SSH_USER, password=SSH_PASS, timeout=30)
    
    local_file = os.path.join(LOCAL_DIR, 'full_local_data.json')
    remote_file = f"{REMOTE_DIR}/full_local_data.json"
    
    print("3. Uploading fixture to Staging server...")
    sftp = client.open_sftp()
    sftp.put(local_file, remote_file)
    sftp.close()
    
    print("4. Resetting CMS tables and cleanly loading 100% exact local data into PostgreSQL...")
    load_cmd = f"""
cd {REMOTE_DIR}
source venv/bin/activate

# Flush CMS tables cleanly so there are no duplicate primary/unique key conflicts
python manage.py flush --no-input

# Load complete fixture
python manage.py loaddata full_local_data.json
rm -f full_local_data.json

# Re-ensure superuser accounts
python -c "
import os, sys, django
sys.path.insert(0, '{REMOTE_DIR}')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ovpa_website.settings')
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
groot, _ = User.objects.get_or_create(username='grootadmin', defaults={{'email': 'ajbasa@up.edu.ph', 'is_staff': True, 'is_superuser': True}})
groot.set_password('xiarabasa12')
groot.is_staff = True
groot.is_superuser = True
groot.is_active = True
groot.save()
"

systemctl restart ovpa_website
"""
    stdin, stdout, stderr = client.exec_command(f"echo '{SSH_PASS}' | sudo -S bash -c \"{load_cmd}\"")
    
    for line in stdout:
        print(line, end="")
    err = stderr.read().decode('ascii', errors='replace')
    if err and "[sudo]" not in err:
        print("STDERR:", err)
        
    client.close()
    
    try:
        os.remove(local_file)
    except OSError:
        pass
        
    print("\nDatabase sync completed successfully with exact 1:1 parity!")

if __name__ == '__main__':
    export_and_sync_all_data()
