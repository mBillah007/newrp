#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# ৪. 🎯 অটো-সুপারইউজার বা অ্যাডমিন ইউজার তৈরি করা
if [ "$CREATE_SUPERUSER" ]
then
  python manage.py createsuperuser --noinput || true
fi