import paramiko
import sys

HOSTNAME = '172.20.7.172'
PORT = 21712
SSH_USER = 'ajbasa'
SSH_PASS = r'H[r=hm5CtQbp{SvzA'

def fix_socket_gunicorn():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOSTNAME, port=PORT, username=SSH_USER, password=SSH_PASS, timeout=20)
    
    sftp = client.open_sftp()
    
    # 1. Update Gunicorn service to use 127.0.0.1:8000 (standard and avoids /run permission issues on Ubuntu 26.04)
    gunicorn_svc = """[Unit]
Description=Gunicorn daemon for OVPA Website
After=network.target

[Service]
User=ajbasa
Group=www-data
WorkingDirectory=/var/www/ovpa_website
ExecStart=/var/www/ovpa_website/venv/bin/gunicorn --access-logfile - --workers 3 --bind 127.0.0.1:8000 ovpa_website.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with sftp.file('/tmp/ovpa_website.service', 'w') as f:
        f.write(gunicorn_svc)
        
    # 2. Update Nginx to proxy to 127.0.0.1:8000
    nginx_conf = """server {
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
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_pass http://127.0.0.1:8000;
    }
}
"""
    with sftp.file('/tmp/ovpa_nginx.conf', 'w') as f:
        f.write(nginx_conf)
        
    sftp.close()
    
    cmd = f"""
echo '{SSH_PASS}' | sudo -S bash -c "
cp /tmp/ovpa_website.service /etc/systemd/system/ovpa_website.service
cp /tmp/ovpa_nginx.conf /etc/nginx/sites-available/ovpa_website
ln -sf /etc/nginx/sites-available/ovpa_website /etc/nginx/sites-enabled/ovpa_website
rm -f /etc/nginx/sites-enabled/default

systemctl daemon-reload
systemctl restart ovpa_website
nginx -t
systemctl restart nginx

sleep 2
systemctl is-active ovpa_website
systemctl is-active nginx
"
"""
    stdin, stdout, stderr = client.exec_command(cmd)
    sys.stdout.buffer.write(stdout.read())
    sys.stdout.flush()
    client.close()

if __name__ == '__main__':
    fix_socket_gunicorn()
