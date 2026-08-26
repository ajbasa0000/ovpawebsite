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

def log(msg):
    try:
        print(f"[MIRROR] {msg}")
    except UnicodeEncodeError:
        sys.stdout.buffer.write(f"[MIRROR] {msg}\n".encode('ascii', errors='replace'))
        sys.stdout.flush()

def run_local(cmd):
    log(f"Running locally: {cmd}")
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=LOCAL_DIR)
    if res.stdout:
        log(res.stdout.strip())
    if res.stderr and res.returncode != 0:
        log(f"ERROR: {res.stderr.strip()}")
    return res.returncode == 0

def sync_media_files(sftp, local_dir, remote_dir):
    try:
        sftp.mkdir(remote_dir)
    except IOError:
        pass

    for item in os.listdir(local_dir):
        local_path = os.path.join(local_dir, item)
        remote_path = remote_dir + '/' + item
        if os.path.isdir(local_path):
            sync_media_files(sftp, local_path, remote_path)
        else:
            try:
                sftp.put(local_path, remote_path)
            except Exception:
                pass

def dump_and_sync_database(client, sftp):
    log("Exporting local database content fixtures...")
    dump_cmd = "python manage.py dumpdata cms accounts auth.group --natural-foreign --natural-primary --indent 2 -o local_data_dump.json"
    run_local(dump_cmd)
    
    local_dump_file = os.path.join(LOCAL_DIR, 'local_data_dump.json')
    remote_dump_file = f"{REMOTE_DIR}/local_data_dump.json"
    
    if os.path.exists(local_dump_file):
        log("Uploading fixtures to staging server...")
        sftp.put(local_dump_file, remote_dump_file)
        
        log("Loading fixtures into staging PostgreSQL...")
        load_script = f"""
cd {REMOTE_DIR}
source venv/bin/activate
python manage.py loaddata local_data_dump.json || true
rm -f local_data_dump.json
"""
        stdin, stdout, stderr = client.exec_command(f"echo '{SSH_PASS}' | sudo -S bash -c \"{load_script}\"")
        out = stdout.read().decode('ascii', errors='replace')
        log(out)
        
        try:
            os.remove(local_dump_file)
        except OSError:
            pass

def main():
    commit_msg = sys.argv[1] if len(sys.argv) > 1 else "Surgical 1:1 mirror sync"
    
    log("=" * 60)
    log(f"SURGICAL 1:1 MIRROR: LOCAL -> STAGING ({HOSTNAME})")
    log("=" * 60)

    # 1. Local Git Commit & Push
    run_local("git add .")
    run_local(f'git commit -m "{commit_msg}"')
    run_local("git push origin master")

    # 2. Connect to SSH
    log("Connecting to Staging Server via SSH...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOSTNAME, port=PORT, username=SSH_USER, password=SSH_PASS, timeout=30)
    log("Connected.")

    sftp = client.open_sftp()

    # 3. Sync media files
    log("Syncing all media uploads and assets...")
    local_media = os.path.join(LOCAL_DIR, 'media')
    if os.path.exists(local_media):
        sync_media_files(sftp, local_media, f"{REMOTE_DIR}/media")

    # 4. Pull Git commits & Run Migrations
    remote_script = f"""
set -e
cd {REMOTE_DIR}
echo "--> Pulling latest git commits..."
git pull origin master

echo "--> Applying database migrations..."
source venv/bin/activate
python manage.py migrate

echo "--> Collecting static files..."
python manage.py collectstatic --noinput

echo "--> Setting permissions..."
chown -R {SSH_USER}:www-data {REMOTE_DIR}/media {REMOTE_DIR}/logs
chmod -R 775 {REMOTE_DIR}/media {REMOTE_DIR}/logs
"""
    cmd = f"echo '{SSH_PASS}' | sudo -S bash -c \"{remote_script}\""
    stdin, stdout, stderr = client.exec_command(cmd)
    for line in stdout:
        log(line.strip())

    # 5. Database Data Parity Sync
    dump_and_sync_database(client, sftp)
    sftp.close()

    # 6. Ensure grootadmin exists with password
    ensure_groot = f"""
cd {REMOTE_DIR}
source venv/bin/activate
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
systemctl reload nginx
"""
    client.exec_command(f"echo '{SSH_PASS}' | sudo -S bash -c \"{ensure_groot}\"")
    client.close()

    log("=" * 60)
    log("1:1 SURGICAL MIRROR COMPLETE!")
    log("Website: http://ovpa-dev.up.edu.ph/")
    log("Admin:   http://ovpa-dev.up.edu.ph/admin/")
    log("=" * 60)

if __name__ == '__main__':
    main()
