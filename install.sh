#! /bin/sh

cd stellar

pip3 freeze > requirements.txt

pip3 install django==3.2.9

pip3 install -U stellar-sdk

pip3 install qrcode[pil]

python3 manage.py migrate

python3 manage.py runserver