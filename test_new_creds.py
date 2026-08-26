import paramiko
import sys

HOSTNAME = '172.20.7.172'
PORT = 21712
USERNAME = 'ajbasa'
PASSWORD = r'H[=hm5CtQbp{SvzA'

def test_login():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(HOSTNAME, port=PORT, username=USERNAME, password=PASSWORD, timeout=10)
        stdin, stdout, stderr = client.exec_command('whoami && uname -a')
        print("SSH Login SUCCESS with new password:")
        print(stdout.read().decode())
        client.close()
    except Exception as e:
        print("SSH Login FAILED with new password:", e)
        # Try original password
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(HOSTNAME, port=PORT, username=USERNAME, password=r'H[r=hm5CtQbp{SvzA', timeout=10)
            stdin, stdout, stderr = client.exec_command('whoami && uname -a')
            print("SSH Login SUCCESS with password 'H[r=hm5CtQbp{SvzA':")
            print(stdout.read().decode())
            client.close()
        except Exception as e2:
            print("SSH Login FAILED with original password too:", e2)

if __name__ == '__main__':
    test_login()
