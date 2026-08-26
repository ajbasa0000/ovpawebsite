import paramiko

HOSTNAME = '172.20.7.172'
PORT = 21712
USERNAME = 'ajbasa'
PASSWORD = r'H[r=hm5CtQbp{SvzA'

def fix():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOSTNAME, port=PORT, username=USERNAME, password=PASSWORD, timeout=20)
    
    sftp = client.open_sftp()
    remote_script_path = '/tmp/setup_pg2.sh'
    
    # Notice the password contains $7 and {4fP_3}, so in bash/SQL single quotes must be handled carefully.
    script_content = """#!/bin/bash
set -e

sudo -u postgres psql << 'EOF'
ALTER USER ovpa_admin WITH PASSWORD '9x-Z-]@k&dT$7(gE{4fP_3}r';
GRANT ALL PRIVILEGES ON DATABASE ovpa_db TO ovpa_admin;
GRANT ALL ON SCHEMA public TO ovpa_admin;
EOF

echo "Password reset executed."
"""
    with sftp.file(remote_script_path, 'w') as f:
        f.write(script_content)
    sftp.close()
    
    cmd = f"echo '{PASSWORD}' | sudo -S bash {remote_script_path}"
    stdin, stdout, stderr = client.exec_command(cmd)
    print(stdout.read().decode())
    print("STDERR:", stderr.read().decode())
    
    # Test connection
    print("Testing connection with ovpa_admin:")
    test_cmd = """
PGPASSWORD='9x-Z-]@k&dT$7(gE{4fP_3}r' psql -h 127.0.0.1 -U ovpa_admin -d ovpa_db -c "SELECT current_user, current_database();"
"""
    stdin, stdout, stderr = client.exec_command(test_cmd)
    print("Result:")
    print(stdout.read().decode())
    print("STDERR:", stderr.read().decode())
    
    client.close()

if __name__ == '__main__':
    fix()
