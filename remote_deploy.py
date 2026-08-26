import paramiko

HOSTNAME = '172.20.7.172'
PORT = 21712
USERNAME = 'ajbasa'
PASSWORD = r'H[r=hm5CtQbp{SvzA'

def run():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOSTNAME, port=PORT, username=USERNAME, password=PASSWORD, timeout=30)
    
    cmd = 'sudo -S -u postgres psql -c "\\du" && sudo -u postgres psql -c "\\l"'
    stdin, stdout, stderr = client.exec_command(cmd, get_pty=True)
    stdin.write(PASSWORD + '\n')
    stdin.flush()
    print(stdout.read().decode())
    client.close()

if __name__ == '__main__':
    run()
