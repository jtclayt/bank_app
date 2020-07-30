#!/bin/bash
# Author: Justin Clayton
# This script automates the deploy process for a django project on AWS

# Check required IP is provided
if [ $# -ne 1 ]; then
  echo "Provide only an IP address that the server will be hosted on" 1>&2
  exit 1
fi

# Server setup steps
# sudo apt-get update
# sudo apt-get install nginx
# sudo apt-get install python3-venv # Say yes if prompted
# python3 -m venv venv
# source venv/bin/activate
# pip install -r requirements.txt
# pip install gunicorn

# Modify settings.py
cd bank_app
sed -i "s/DEBUG = True/DEBUG = False/" settings.py
sed -i "s/ALLOWED_HOSTS = \[\]/ALLOWED_HOSTS = \[\'$1\'\]/" settings.py
sed -i "s/\n    os.path.join(BASE_DIR, \"static\"),//" settings.py
echo 'STATIC_ROOT = os.path.join(BASE_DIR, "static/")' >> settings.py


