# stellar-wallet-test
Run the project from the stellar root folder.

cd stellar

Setup:

pip3 freeze > requirements.txt

pip3 install django==3.2.9

pip3 install -U stellar-sdk

pip3 install qrcode[pil]

python3 manage.py runserver 8000


Move money and access new markets.
Intended to enhance rather than undermine or replace the existing financial system.

A valid keypair does not make an account: in order to prevent unused accounts from bloating the ledger, Stellar requires accounts to hold a minimum balance of 1 XLM before they actually exist. Until it gets a bit of funding, your keypair doesn’t warrant space on the ledger.

Current Status

Functionality available for users to create and activate a wallet in the stellar network.
