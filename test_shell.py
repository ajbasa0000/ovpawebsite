import paramiko
import time

def main():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('172.20.7.172', port=21712, username='ajbasa', password='H[r=hm5CtQbp{SvzA')
    
    chan = client.invoke_shell()
    time.sleep(1)
    
    def send_cmd(cmd, wait_time=2):
        chan.send(cmd + '\n')
        time.sleep(wait_time)
        resp = b""
        while chan.recv_ready():
            resp += chan.recv(4096)
        return resp.decode('utf-8', errors='ignore')
    
    print("Initial banner:")
    print(send_cmd(''))
    
    print("Sending sudo psql command:")
    out = send_cmd('sudo -u postgres psql')
    print(out)
    if 'Password:' in out or '[sudo]' in out:
        out2 = send_cmd('H[r=hm5CtQbp{SvzA')
        print("Password output:")
        print(out2)
        
    print("Listing databases and users:")
    print(send_cmd('\\du'))
    print(send_cmd('\\l'))
    print(send_cmd('\\q'))
    
    client.close()

if __name__ == '__main__':
    main()
