import os
import sys
import paramiko
import time

HOSTNAME = '172.20.7.172'
PORT = 21712
SSH_USER = 'ajbasa'
SSH_PASS = r'H[r=hm5CtQbp{SvzA'

def main():
    print("Connecting...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOSTNAME, port=PORT, username=SSH_USER, password=SSH_PASS, timeout=20)
    print("Connected. Executing deployment script...")
    
    cmd = f"echo '{SSH_PASS}' | sudo -S bash /tmp/full_deploy.sh"
    stdin, stdout, stderr = client.exec_command(cmd)
    
    while True:
        line = stdout.readline()
        if not line:
            break
        # Safe print for Windows console
        sys.stdout.buffer.write(line.encode('utf-8', errors='replace'))
        sys.stdout.flush()
        
    err = stderr.read().decode('utf-8', errors='ignore')
    if err:
        print("\nSTDERR (if any):", [l for l in err.splitlines() if '[sudo]' not in l])
        
    client.close()
    print("\n\nAll deployment commands completed!")

if __name__ == '__main__':
    main()
