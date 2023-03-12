#!/usr/bin/env bash
# exit on error
set -o errexit

virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate