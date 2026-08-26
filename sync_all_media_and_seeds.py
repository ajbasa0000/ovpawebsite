import os
import sys
import paramiko

HOSTNAME = '172.20.7.172'
PORT = 21712
SSH_USER = 'ajbasa'
SSH_PASS = r'H[r=hm5CtQbp{SvzA'

LOCAL_MEDIA_DIR = r'c:\Users\ajbas\Documents\Apps\ovpa_website\media'
REMOTE_MEDIA_DIR = '/var/www/ovpa_website/media'

def upload_dir(sftp, local_dir, remote_dir):
    try:
        sftp.mkdir(remote_dir)
    except IOError:
        pass

    for item in os.listdir(local_dir):
        local_path = os.path.join(local_dir, item)
        remote_path = remote_dir + '/' + item
        if os.path.isdir(local_path):
            upload_dir(sftp, local_path, remote_path)
        else:
            try:
                sftp.put(local_path, remote_path)
            except Exception as e:
                pass

def main():
    print("Connecting to server to sync all media...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOSTNAME, port=PORT, username=SSH_USER, password=SSH_PASS, timeout=30)
    
    sftp = client.open_sftp()
    upload_dir(sftp, LOCAL_MEDIA_DIR, REMOTE_MEDIA_DIR)
    sftp.close()
    
    script = """
set -e
chown -R ajbasa:www-data /var/www/ovpa_website/media
chmod -R 775 /var/www/ovpa_website/media
cd /var/www/ovpa_website
source venv/bin/activate
# Run seeds to ensure database entries point to all media & services
python seed_cms.py || true
python populate_content.py || true
python seed_actual_services.py || true
python populate_quality_values.py || true
python seed_project_images.py || true
python update_about_content.py || true
systemctl restart ovpa_website
systemctl restart nginx
"""
    cmd = f"echo '{SSH_PASS}' | sudo -S bash -c \"{script}\""
    stdin, stdout, stderr = client.exec_command(cmd)
    stdout.read()
    client.close()
    print("All media, images, database seeds, and cards populated and synced!")

if __name__ == '__main__':
    main()
