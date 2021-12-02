from django.shortcuts import render
from django.http import HttpResponse
from stellar_sdk.keypair import Keypair
from stellar_sdk import Server, exceptions
from django.conf import settings
import qrcode
import os


def index(request):
    template = 'wallet/index.html'
    return render(request, template, {})

def create(request):
    template = 'wallet/create.html'
    # Generate a random keypair
    new_account = Keypair.random()
    # Load required variables into template
    context = {
        'public_key': new_account.public_key,
        'secret': new_account.secret
    }
    return render(request, template, context)

def account(request):
    template = 'wallet/account.html'
    return render(request, template, {})

def activate(request):
    dirName = 'media/'
    try:
        # Create Directory
        os.mkdir(dirName)
        print("Directory " , dirName ,  " Created ") 
    except FileExistsError:
        print("Directory " , dirName ,  " already exists")

    media_dir = dirName
    template = 'wallet/activate.html'
    horizon_url = "https://horizon.stellar.org"
    server = Server(horizon_url)
    # Get user secret
    secret = request.POST.get('secret', '')
    # Generate keypair from secret
    new_account = Keypair.from_secret(secret)
    # Begin account activation.
    public_key = new_account.public_key
     # Check if the new account exists on the stellar network. 
     # It has to funded with the minimum balance of 5 XML before activation.
    try:
        account = server.load_account(account_id=public_key)
    except exceptions.NotFoundError:
        # Generate QR code and deposit instructions
        img = qrcode.make(public_key)
        type(img)  # qrcode.image.pil.PilImage
        img.save(media_dir + public_key + ".png")

    QRurl = '../' + media_dir + public_key + ".png"
    # Load required variables into template
    context = {
        'public_key': public_key,
        'qr': QRurl
    }
    return render(request, template, context)