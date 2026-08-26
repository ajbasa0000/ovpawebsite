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
    except Exception:
        sys.stdout.buffer.write(f"[MIRROR] {msg}\n".encode('ascii', errors='replace'))
        sys.stdout.flush()

def run_local(cmd):
    log(f"Running locally: {cmd}")
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=LOCAL_DIR, env=env, encoding='utf-8')
    if res.stdout:
        log(res.stdout.strip())
    if res.stderr and res.returncode != 0:
        log(f"ERROR: {res.stderr.strip()}")
    return res.returncode == 0

def run_remote_step(client, cmd_desc, command):
    log(f"--> {cmd_desc}...")
    full_cmd = f"echo '{SSH_PASS}' | sudo -S bash -c \"{command}\""
    stdin, stdout, stderr = client.exec_command(full_cmd)
    out = stdout.read().decode('ascii', errors='replace').strip()
    err = stderr.read().decode('ascii', errors='replace').strip()
    if out:
        log(f"    {out}")
    if err and "[sudo]" not in err and "WARNING" not in err:
        log(f"    [ERR] {err}")

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
    log("Exporting local database content fixtures in UTF-8...")
    local_dump_file = os.path.join(LOCAL_DIR, 'local_data_dump.json')
    remote_dump_file = f"{REMOTE_DIR}/local_data_dump.json"
    
    dump_script = """import os, sys, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ovpa_website.settings')
django.setup()
from django.core.management import call_command
with open('local_data_dump.json', 'w', encoding='utf-8') as f:
    call_command('dumpdata', 'cms', 'accounts', 'auth.group', natural_foreign=True, natural_primary=True, indent=2, stdout=f)
print('DUMP_SUCCESS')
"""
    subprocess.run([sys.executable, "-c", dump_script], cwd=LOCAL_DIR)
    
    if os.path.exists(local_dump_file):
        log("Uploading database fixtures to staging server...")
        sftp.put(local_dump_file, remote_dump_file)
        
        load_script = f"""
cd {REMOTE_DIR}
source venv/bin/activate
python manage.py loaddata local_data_dump.json || true
rm -f local_data_dump.json
"""
        run_remote_step(client, "Loading database fixtures into PostgreSQL", load_script)
        
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

    # 4. Force Reset Git to Origin/Master & Run Migrations & Collect Static
    run_remote_step(client, "Force-syncing code with origin/master", f"cd {REMOTE_DIR} && git fetch origin master && git reset --hard origin/master")
    run_remote_step(client, "Applying database migrations", f"cd {REMOTE_DIR} && source venv/bin/activate && python manage.py migrate")
    run_remote_step(client, "Collecting static files", f"cd {REMOTE_DIR} && source venv/bin/activate && python manage.py collectstatic --noinput")
    run_remote_step(client, "Setting directory permissions", f"chown -R {SSH_USER}:www-data {REMOTE_DIR}/media {REMOTE_DIR}/logs && chmod -R 775 {REMOTE_DIR}/media {REMOTE_DIR}/logs")

    # 5. Database Data Parity Sync
    dump_and_sync_database(client, sftp)
    sftp.close()

    # 6. Ensure grootadmin exists and restart Gunicorn
    ensure_and_restart = f"""
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
    run_remote_step(client, "Verifying superuser & reloading Gunicorn/Nginx", ensure_and_restart)
    client.close()

    log("=" * 60)
    log("1:1 SURGICAL MIRROR COMPLETE!")
    log("Website: http://ovpa-dev.up.edu.ph/")
    log("Admin:   http://ovpa-dev.up.edu.ph/admin/")
    log("=" * 60)

if __name__ == '__main__':
    main()
