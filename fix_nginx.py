import paramiko

HOSTNAME = '172.20.7.172'
PORT = 21712
SSH_USER = 'ajbasa'
SSH_PASS = r'H[r=hm5CtQbp{SvzA'

def fix_nginx():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOSTNAME, port=PORT, username=SSH_USER, password=SSH_PASS, timeout=20)
    
    script = """#!/bin/bash
set -e

# Fix Nginx default proxy_params if missing
cat << 'PROXY' > /etc/nginx/proxy_params
proxy_set_header Host $http_host;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;
PROXY

# Fix Nginx site config
cat << 'NGINX' > /etc/nginx/sites-available/ovpa_website
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name 172.20.7.172 dev-ovpawebsite.up.edu.ph _;

    client_max_body_size 50M;

    location /static/ {
        alias /var/www/ovpa_website/staticfiles/;
    }

    location /media/ {
        alias /var/www/ovpa_website/media/;
    }

    location / {
        include /etc/nginx/proxy_params;
        proxy_pass http://unix:/run/gunicorn_ovpa.sock;
    }
}
NGINX

ln -sf /etc/nginx/sites-available/ovpa_website /etc/nginx/sites-enabled/ovpa_website
rm -f /etc/nginx/sites-enabled/default

# Set permissions for socket directory
chmod 755 /run
chown -R ajbasa:www-data /var/www/ovpa_website
chmod -R 775 /var/www/ovpa_website

systemctl restart ovpa_website
nginx -t
systemctl restart nginx

sleep 2
echo "--- Testing Gunicorn socket ---"
ls -la /run/gunicorn_ovpa.sock
echo "--- Testing HTTP internal request ---"
python3 -c "import urllib.request; print('INTERNAL HTTP CODE:', urllib.request.urlopen('http://127.0.0.1/').getcode())"
"""
    cmd = f"echo '{SSH_PASS}' | sudo -S bash -c \"{script}\""
    stdin, stdout, stderr = client.exec_command(cmd)
    out = stdout.read().decode('ascii', errors='replace')
    print("OUTPUT:\n", out)
    err = stderr.read().decode('ascii', errors='replace')
    print("STDERR:\n", [l for l in err.splitlines() if '[sudo]' not in l])
    client.close()

if __name__ == '__main__':
    fix_nginx()
