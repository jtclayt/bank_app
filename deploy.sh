#!/bin/bash
# Author: Justin Clayton
# This script automates the deploy process for a django project on AWS
# Make sure to create .env file with secret key before running!
# Hit y on prompts if they come up.

# Check required IP is provided
if [ $# -ne 1 ]; then
  echo "Provide only an IP address that the server will be hosted on" 1>&2
  exit 1
fi

# Server setup steps
sudo apt-get update
sudo apt-get install nginx
sudo apt-get install python3-venv # Say yes if prompted
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn

# Modify settings.py
cd bank_app
sed -i "s/DEBUG = True/DEBUG = False/" settings.py
sed -i "s/ALLOWED_HOSTS = \[\]/ALLOWED_HOSTS = \[\'$1\'\]/" settings.py
sed -i "s/    os.path.join(BASE_DIR, \"static\"),//" settings.py
echo 'STATIC_ROOT = os.path.join(BASE_DIR, "static/")' >> settings.py
cd ..
python manage.py collectstatic # say yes if prompted
python manage.py makemigrations users
python manage.py makemigrations app
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata app/data/app.json

# Gunicorn setup steps
sudo touch /etc/systemd/system/gunicorn.service
sudo chmod 666 /etc/systemd/system/gunicorn.service
sudo cat deploy/gunicorn.txt > /etc/systemd/system/gunicorn.service
sudo systemctl daemon-reload
sudo systemctl restart gunicorn

# NGINX setup steps
sudo touch /etc/nginx/sites-available/bank_app
sudo chmod 666 /etc/nginx/sites-available/bank_app
sudo cat deploy/nginx.txt | sed "s/server_name/server_name $1/" > /etc/nginx/sites-available/bank_app
sudo ln -s /etc/nginx/sites-available/bank_app /etc/nginx/sites-enabled
sudo nginx -t
sudo rm /etc/nginx/sites-enabled/default
sudo service nginx restart
