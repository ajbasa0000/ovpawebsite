import paramiko

HOSTNAME = '172.20.7.172'
PORT = 21712
USERNAME = 'ajbasa'
PASSWORD = r'H[r=hm5CtQbp{SvzA'

def fix():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOSTNAME, port=PORT, username=USERNAME, password=PASSWORD, timeout=20)
    
    cmd = """
echo 'H[r=hm5CtQbp{SvzA' | sudo -S bash -c "
find /etc/postgresql/ -name pg_hba.conf
"
"""
    stdin, stdout, stderr = client.exec_command(cmd)
    print("pg_hba.conf files:")
    print(stdout.read().decode())
    print("STDERR:", stderr.read().decode())
    client.close()

if __name__ == '__main__':
    fix()
