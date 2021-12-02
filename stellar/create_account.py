from stellar_sdk.keypair import Keypair
import requests
# Configure StellarSdk to talk to the horizon instance hosted by Stellar.org
horizon_url = "https://horizon.stellar.org"

account = Keypair.random()
secret = account.secret
public_key = account.public_key

