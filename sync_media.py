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
            print(f"Uploading {item} -> {remote_path}")
            sftp.put(local_path, remote_path)

def main():
    print("Connecting to server to sync media files...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOSTNAME, port=PORT, username=SSH_USER, password=SSH_PASS, timeout=30)
    
    sftp = client.open_sftp()
    upload_dir(sftp, LOCAL_MEDIA_DIR, REMOTE_MEDIA_DIR)
    sftp.close()
    
    # Ensure correct permissions on remote media
    cmd = f"echo '{SSH_PASS}' | sudo -S bash -c \"chown -R ajbasa:www-data /var/www/ovpa_website/media && chmod -R 775 /var/www/ovpa_website/media && systemctl restart ovpa_website nginx\""
    stdin, stdout, stderr = client.exec_command(cmd)
    stdout.read()
    client.close()
    print("Media sync complete!")

if __name__ == '__main__':
    main()
