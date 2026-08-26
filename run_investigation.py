import paramiko
import sys

HOSTNAME = '172.20.7.172'
PORT = 21712
SSH_USER = 'ajbasa'
SSH_PASS = r'H[r=hm5CtQbp{SvzA'

def run_investigation():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOSTNAME, port=PORT, username=SSH_USER, password=SSH_PASS, timeout=20)
    
    commands = [
        "cd /var/www/ovpa_website && git log -n 1 --oneline",
        "cd /var/www/ovpa_website && git fetch origin master && git reset --hard origin/master",
        "cd /var/www/ovpa_website && git log -n 1 --oneline",
        "grep -n 'UP-Seal' /var/www/ovpa_website/templates/base.html || true",
        "systemctl restart ovpa_website",
        "systemctl reload nginx",
    ]
    
    for cmd in commands:
        full_cmd = f"echo '{SSH_PASS}' | sudo -S bash -c \"{cmd}\""
        stdin, stdout, stderr = client.exec_command(full_cmd)
        out = stdout.read().decode('ascii', errors='replace').strip()
        err = stderr.read().decode('ascii', errors='replace').strip()
        print(f"CMD: {cmd}")
        print(f"OUT: {out}")
        if err and "[sudo]" not in err:
            print(f"ERR: {err}")
        print("-" * 40)
        
    client.close()

if __name__ == '__main__':
    run_investigation()
