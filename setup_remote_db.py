import paramiko
import os
import sys

HOSTNAME = '172.20.7.172'
PORT = 21712
USERNAME = 'ajbasa'
PASSWORD = r'H[r=hm5CtQbp{SvzA'

def run():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print("Connecting...")
    client.connect(HOSTNAME, port=PORT, username=USERNAME, password=PASSWORD, timeout=20)
    print("Connected.")
    
    # 1. Reset/ensure postgres user and database
    setup_db_script = """
set -e
sudo -S -k -- sh -c '
sudo -u postgres psql -c "ALTER USER ovpa_admin WITH PASSWORD '\''9x-Z-]@k&dT$7(gE{4fP_3}r'\'';" || sudo -u postgres psql -c "CREATE USER ovpa_admin WITH PASSWORD '\''9x-Z-]@k&dT$7(gE{4fP_3}r'\'';"
sudo -u postgres psql -c "CREATE DATABASE ovpa_db OWNER ovpa_admin;" || true
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE ovpa_db TO ovpa_admin;"
'
"""
    print("Running setup_db...")
    stdin, stdout, stderr = client.exec_command(f"echo '{PASSWORD}' | sudo -S bash -c \"sudo -u postgres psql -c \\\"ALTER USER ovpa_admin WITH PASSWORD '9x-Z-]@k&dT$7(gE{{4fP_3}}r';\\\" 2>&1 || sudo -u postgres psql -c \\\"CREATE USER ovpa_admin WITH PASSWORD '9x-Z-]@k&dT$7(gE{{4fP_3}}r';\\\" 2>&1; sudo -u postgres psql -c \\\"CREATE DATABASE ovpa_db OWNER ovpa_admin;\\\" 2>&1 || true; sudo -u postgres psql -c \\\"GRANT ALL PRIVILEGES ON DATABASE ovpa_db TO ovpa_admin;\\\" 2>&1\"")
    print(stdout.read().decode('utf-8', errors='ignore'))
    print("STDERR:", stderr.read().decode('utf-8', errors='ignore'))
    
    # Check test connection
    print("Testing psql connection as ovpa_admin...")
    stdin, stdout, stderr = client.exec_command('PGPASSWORD="9x-Z-]@k&dT$7(gE{4fP_3}r" psql -h 127.0.0.1 -U ovpa_admin -d ovpa_db -c "SELECT current_user, current_database();"')
    print(stdout.read().decode('utf-8', errors='ignore'))
    print("STDERR:", stderr.read().decode('utf-8', errors='ignore'))
    
    client.close()

if __name__ == '__main__':
    run()
