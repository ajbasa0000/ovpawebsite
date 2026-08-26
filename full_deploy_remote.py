import os
import sys
import paramiko
import time

HOSTNAME = '172.20.7.172'
PORT = 21712
SSH_USER = 'ajbasa'
SSH_PASS = r'H[r=hm5CtQbp{SvzA'

PG_ROOT_USER = 'postgres'
PG_ROOT_PASS = r'@)YGWZ}4QBcpuCXPm=H2-5-kd'

APP_DIR = '/var/www/ovpa_website'
GIT_REPO = 'https://github.com/ajbasa0000/ovpawebsite.git'

def log(msg):
    print(f"\n[DEPLOY] {msg}")

def main():
    log("Connecting to remote server via SSH...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOSTNAME, port=PORT, username=SSH_USER, password=SSH_PASS, timeout=20)
    log("SSH Connection Successful.")
    
    sftp = client.open_sftp()
    
    # 1. Setup deployment bash script on server
    deploy_script = """#!/bin/bash
set -e

echo "=== 1. Setting up PostgreSQL database & user ==="
PGPASSWORD='@)YGWZ}4QBcpuCXPm=H2-5-kd' psql -h 127.0.0.1 -U postgres << 'EOF'
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'ovpa_admin') THEN
        CREATE ROLE ovpa_admin WITH LOGIN PASSWORD '9x-ZJ@k&dT$7(gE{4fP_3}r';
    ELSE
        ALTER ROLE ovpa_admin WITH PASSWORD '9x-ZJ@k&dT$7(gE{4fP_3}r';
    END IF;
END $$;
EOF

PGPASSWORD='@)YGWZ}4QBcpuCXPm=H2-5-kd' psql -h 127.0.0.1 -U postgres -tc "SELECT 1 FROM pg_database WHERE datname = 'ovpa_db'" | grep -q 1 || \
PGPASSWORD='@)YGWZ}4QBcpuCXPm=H2-5-kd' psql -h 127.0.0.1 -U postgres -c "CREATE DATABASE ovpa_db OWNER ovpa_admin;"

PGPASSWORD='@)YGWZ}4QBcpuCXPm=H2-5-kd' psql -h 127.0.0.1 -U postgres -d ovpa_db -c "GRANT ALL PRIVILEGES ON DATABASE ovpa_db TO ovpa_admin;"
PGPASSWORD='@)YGWZ}4QBcpuCXPm=H2-5-kd' psql -h 127.0.0.1 -U postgres -d ovpa_db -c "GRANT ALL ON SCHEMA public TO ovpa_admin;"

echo "=== 2. Creating web directory and permissions ==="
mkdir -p /var/www/ovpa_website
chown -R ajbasa:www-data /var/www/ovpa_website
chmod -R 775 /var/www/ovpa_website

echo "=== 3. Cloning/Updating Git Repository ==="
if [ ! -d "/var/www/ovpa_website/.git" ]; then
    git clone https://github.com/ajbasa0000/ovpawebsite.git /var/www/ovpa_website
else
    cd /var/www/ovpa_website && git pull origin master
fi

cd /var/www/ovpa_website

echo "=== 4. Setting up Python Virtual Environment ==="
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt gunicorn psycopg2-binary

echo "=== 5. Writing production .env ==="
cat << 'ENVFILE' > /var/www/ovpa_website/.env
DEBUG=False
SECRET_KEY=django-insecure-ovpa-staging-prod-key-up-edu-ph-2026
ALLOWED_HOSTS=172.20.7.172,dev-ovpawebsite.up.edu.ph,localhost,127.0.0.1
DB_ENGINE=django.db.backends.postgresql
DB_NAME=ovpa_db
DB_USER=ovpa_admin
DB_PASSWORD=9x-ZJ@k&dT$7(gE{4fP_3}r
DB_HOST=127.0.0.1
DB_PORT=5432
ENVFILE

echo "=== 6. Running Migrations and Static Collection ==="
python manage.py migrate
python manage.py collectstatic --noinput

# Auto-create admin user if not existing
python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ovpa_website.settings')
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'ajbasa@up.edu.ph', 'Admin@OVPA2026!')
    print('Superuser created: admin / Admin@OVPA2026!')
else:
    print('Superuser already exists.')
"

# Seed CMS content if scripts exist
if [ -f "seed_cms.py" ]; then
    python seed_cms.py || true
fi
if [ -f "populate_content.py" ]; then
    python populate_content.py || true
fi
if [ -f "seed_actual_services.py" ]; then
    python seed_actual_services.py || true
fi

echo "=== 7. Configuring Gunicorn Systemd Service ==="
cat << 'SVC' > /etc/systemd/system/ovpa_website.service
[Unit]
Description=Gunicorn daemon for OVPA Website
After=network.target

[Service]
User=ajbasa
Group=www-data
WorkingDirectory=/var/www/ovpa_website
ExecStart=/var/www/ovpa_website/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/run/gunicorn_ovpa.sock ovpa_website.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
SVC

systemctl daemon-reload
systemctl enable ovpa_website
systemctl restart ovpa_website

echo "=== 8. Configuring Nginx ==="
cat << 'NGINXCONF' > /etc/nginx/sites-available/ovpa_website
server {
    listen 80;
    server_name 172.20.7.172 dev-ovpawebsite.up.edu.ph;

    client_max_body_size 50M;

    location /static/ {
        alias /var/www/ovpa_website/staticfiles/;
    }

    location /media/ {
        alias /var/www/ovpa_website/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn_ovpa.sock;
    }
}
NGINXCONF

ln -sf /etc/nginx/sites-available/ovpa_website /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

nginx -t
systemctl restart nginx

echo "=== DEPLOYMENT COMPLETED SUCCESSFULLY ==="
"""
    
    remote_script_path = '/tmp/full_deploy.sh'
    with sftp.file(remote_script_path, 'w') as f:
        f.write(deploy_script)
    sftp.close()
    
    log("Uploaded deployment script. Executing on server with sudo...")
    cmd = f"echo '{SSH_PASS}' | sudo -S bash {remote_script_path}"
    stdin, stdout, stderr = client.exec_command(cmd)
    
    for line in iter(stdout.readline, ""):
        print(line, end="")
        
    err = stderr.read().decode('utf-8', errors='ignore')
    if err and not "[sudo: authenticate]" in err:
        print("\nSTDERR:", err)
        
    client.close()
    log("Deployment process finished!")

if __name__ == '__main__':
    main()
