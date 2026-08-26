import paramiko

HOSTNAME = '172.20.7.172'
PORT = 21712
SSH_USER = 'ajbasa'
SSH_PASS = r'H[r=hm5CtQbp{SvzA'

def check_ports():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOSTNAME, port=PORT, username=SSH_USER, password=SSH_PASS, timeout=20)
    
    cmd = "sudo ss -tulpn"
    stdin, stdout, stderr = client.exec_command(f"echo '{SSH_PASS}' | sudo -S {cmd}")
    for line in stdout:
        print(line.strip())
    client.close()

if __name__ == '__main__':
    check_ports()
