import paramiko
import sys

HOSTNAME = '172.20.7.172'
PORT = 21712
SSH_USER = 'ajbasa'
SSH_PASS = r'H[r=hm5CtQbp{SvzA'

def fix_domain_and_deploy():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOSTNAME, port=PORT, username=SSH_USER, password=SSH_PASS, timeout=20)
    
    script = """
set -e
cd /var/www/ovpa_website
git pull origin master

# Update .env to allow ovpa-dev.up.edu.ph and wildcards
cat << 'ENV' > /var/www/ovpa_website/.env
DEBUG=False
SECRET_KEY=django-insecure-ovpa-staging-prod-key-up-edu-ph-2026
ALLOWED_HOSTS=ovpa-dev.up.edu.ph,dev-ovpawebsite.up.edu.ph,172.20.7.172,localhost,127.0.0.1,*
DB_ENGINE=django.db.backends.postgresql
DB_NAME=ovpa_db
DB_USER=ovpa_admin
DB_PASSWORD=9x-ZJ@k&dT$7(gE{4fP_3}r
DB_HOST=127.0.0.1
DB_PORT=5432
ENV

# Update Nginx server_name to include ovpa-dev.up.edu.ph
cat << 'NGINX' > /etc/nginx/sites-available/ovpa_website
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name ovpa-dev.up.edu.ph dev-ovpawebsite.up.edu.ph 172.20.7.172 _;

    client_max_body_size 50M;

    location /static/ {
        alias /var/www/ovpa_website/staticfiles/;
    }

    location /media/ {
        alias /var/www/ovpa_website/media/;
    }

    location / {
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_pass http://127.0.0.1:8000;
    }
}
NGINX

source venv/bin/activate
python manage.py collectstatic --noinput

systemctl daemon-reload
systemctl restart ovpa_website
systemctl restart nginx

sleep 2
echo "=== TESTING HTTP ON DOMAIN ==="
curl -s -I -H "Host: ovpa-dev.up.edu.ph" http://127.0.0.1/ | head -n 5
"""
    cmd = f"echo '{SSH_PASS}' | sudo -S bash -c \"{script}\""
    stdin, stdout, stderr = client.exec_command(cmd)
    sys.stdout.buffer.write(stdout.read())
    sys.stdout.flush()
    client.close()

if __name__ == '__main__':
    fix_domain_and_deploy()
