from django.test import TestCase
from stellar_sdk.keypair import Keypair
from stellar_sdk import Server, exceptions
import qrcode

horizon_url = "https://horizon.stellar.org"
server = Server(horizon_url)
# Generate keypair from secret
secret = 'SBGM26AWP2OGFKWXNU7BUYM4GJBLMFQRKKG3ILGRPHFUQDW75J4BAFXC'
new_account = Keypair.from_secret(secret)
# Begin account activation.
# Check if the new account exists on thge stellar network. If not it has to funded with the minimum balance of 5 XML
public_key = new_account.public_key
try:
    account = server.load_account(account_id=public_key)
except exceptions.NotFoundError:
    print('Not Active Yet!')
# Generate QR code and deposit instructions
img = qrcode.make(public_key)
type(img)  # qrcode.image.pil.PilImage
img.save(public_key+".png")

