import paramiko

HOSTNAME = '172.20.7.172'
PORT = 21712
SSH_USER = 'ajbasa'
SSH_PASS = r'H[r=hm5CtQbp{SvzA'

def fix():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOSTNAME, port=PORT, username=SSH_USER, password=SSH_PASS, timeout=20)
    
    sftp = client.open_sftp()
    
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
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn_ovpa.sock;
    }
}
"""
    with sftp.file('/tmp/ovpa_website.conf', 'w') as f:
        f.write(nginx_conf)
    sftp.close()
    
    cmd = f"""
echo '{SSH_PASS}' | sudo -S bash -c "
cp /tmp/ovpa_website.conf /etc/nginx/sites-available/ovpa_website
ln -sf /etc/nginx/sites-available/ovpa_website /etc/nginx/sites-enabled/ovpa_website
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl restart nginx
systemctl restart ovpa_website
systemctl status ovpa_website --no-pager
"
"""
    stdin, stdout, stderr = client.exec_command(cmd)
    out = stdout.read().decode('ascii', errors='replace')
    print("OUTPUT:\n", out)
    client.close()

if __name__ == '__main__':
    fix()
