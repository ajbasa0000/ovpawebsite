import paramiko
import sys

HOSTNAME = '172.20.7.172'
PORT = 21712
SSH_USER = 'ajbasa'
SSH_PASS = r'H[r=hm5CtQbp{SvzA'

def diagnose():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOSTNAME, port=PORT, username=SSH_USER, password=SSH_PASS, timeout=20)
    
    script = """
cd /var/www/ovpa_website
echo "=== CURRENT GIT HEAD ON STAGING ==="
git log -n 2 --oneline

echo "=== CHECK BASE.HTML FOR UP SEAL IN /var/www/ovpa_website ==="
grep -n "UP-Seal" templates/base.html || echo "UP-Seal NOT IN BASE.HTML"

echo "=== CHECK MEDIA DIRECTORY FOR UP-Seal.png ==="
ls -la /var/www/ovpa_website/media/UP-Seal.png || echo "UP-Seal.png NOT IN MEDIA"

echo "=== CHECK GUNICORN SYSTEMD STATUS ==="
systemctl status ovpa_website --no-pager -n 5

echo "=== FETCHING LIVE HOMEPAGE LOCALLY ON SERVER VIA CURL ==="
curl -s http://127.0.0.1:8000/ | grep -n "UP-Seal" || echo "NOT IN GUNICORN OUTPUT"
"""
    stdin, stdout, stderr = client.exec_command(f"echo '{SSH_PASS}' | sudo -S bash -c \"{script}\"")
    sys.stdout.buffer.write(stdout.read())
    sys.stdout.buffer.write(stderr.read())
    sys.stdout.flush()
    client.close()

if __name__ == '__main__':
    diagnose()
