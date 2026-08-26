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
    remote_script_path = '/tmp/setup_pg.sh'
    
    script_content = """#!/bin/bash
set -e

# Update pg_hba.conf to trust local socket for postgres
if ! grep -q "local   all             postgres                                trust" /etc/postgresql/18/main/pg_hba.conf; then
    sed -i '1s/^/local   all             postgres                                trust\\n/' /etc/postgresql/18/main/pg_hba.conf
fi

systemctl restart postgresql

# Create or alter role
sudo -u postgres psql -c "ALTER ROLE ovpa_admin WITH PASSWORD '9x-Z-]@k&dT\$7(gE{4fP_3}r';" 2>/dev/null || sudo -u postgres psql -c "CREATE ROLE ovpa_admin WITH LOGIN PASSWORD '9x-Z-]@k&dT\$7(gE{4fP_3}r';"

# Create database if not exists
if ! sudo -u postgres psql -lqt | cut -d \\| -f 1 | grep -qw ovpa_db; then
    sudo -u postgres psql -c "CREATE DATABASE ovpa_db OWNER ovpa_admin;"
fi

sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE ovpa_db TO ovpa_admin;"
sudo -u postgres psql -d ovpa_db -c "GRANT ALL ON SCHEMA public TO ovpa_admin;"
echo "POSTGRES_SETUP_COMPLETE"
"""
    with sftp.file(remote_script_path, 'w') as f:
        f.write(script_content)
    sftp.close()
    
    # Execute with sudo
    cmd = f"echo '{PASSWORD}' | sudo -S bash {remote_script_path}"
    stdin, stdout, stderr = client.exec_command(cmd)
    print(stdout.read().decode())
    print("STDERR:", stderr.read().decode())
    
    # Test connection now
    print("Testing connection with ovpa_admin:")
    stdin, stdout, stderr = client.exec_command('PGPASSWORD="9x-Z-]@k&dT$7(gE{4fP_3}r" psql -h 127.0.0.1 -U ovpa_admin -d ovpa_db -c "SELECT current_user, current_database();"')
    print("Result:")
    print(stdout.read().decode())
    print("STDERR:", stderr.read().decode())
    
    client.close()

if __name__ == '__main__':
    fix()
