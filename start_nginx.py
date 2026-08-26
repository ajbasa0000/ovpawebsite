import paramiko

HOSTNAME = '172.20.7.172'
PORT = 21712
SSH_USER = 'ajbasa'
SSH_PASS = r'H[r=hm5CtQbp{SvzA'

def start_nginx():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOSTNAME, port=PORT, username=SSH_USER, password=SSH_PASS, timeout=20)
    
    cmd = """
echo 'H[r=hm5CtQbp{SvzA' | sudo -S bash -c "
nginx -t
systemctl unmask nginx || true
systemctl enable nginx
systemctl start nginx
systemctl status nginx --no-pager
"
"""
    stdin, stdout, stderr = client.exec_command(cmd)
    for line in stdout:
        print(line.strip())
    client.close()

if __name__ == '__main__':
    start_nginx()
