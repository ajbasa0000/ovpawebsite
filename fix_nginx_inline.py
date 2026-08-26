import paramiko

HOSTNAME = '172.20.7.172'
PORT = 21712
SSH_USER = 'ajbasa'
SSH_PASS = r'H[r=hm5CtQbp{SvzA'

def fix_nginx():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOSTNAME, port=PORT, username=SSH_USER, password=SSH_PASS, timeout=20)
    
    sftp = client.open_sftp()
    
    # Standalone nginx config with inline proxy headers (no missing proxy_params file)
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
        proxy_pass http://unix:/run/gunicorn_ovpa.sock;
    }
}
"""
    with sftp.file('/tmp/ovpa_nginx.conf', 'w') as f:
        f.write(nginx_conf)
    sftp.close()
    
    cmd = f"""
echo '{SSH_PASS}' | sudo -S bash -c "
cp /tmp/ovpa_nginx.conf /etc/nginx/sites-available/ovpa_website
ln -sf /etc/nginx/sites-available/ovpa_website /etc/nginx/sites-enabled/ovpa_website
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl restart nginx
systemctl status nginx --no-pager
"
"""
    stdin, stdout, stderr = client.exec_command(cmd)
    for line in stdout:
        print(line.strip())
    client.close()

if __name__ == '__main__':
    fix_nginx()
