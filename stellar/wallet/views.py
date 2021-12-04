from django.shortcuts import render, redirect
from django.http import HttpResponse
from stellar_sdk.keypair import Keypair
from stellar_sdk import Server, exceptions
from django.conf import settings
import qrcode
import os
import requests

# Globals
account_url = settings.HORIZON_LIVE + '/accounts/'

def index(request):
    template = 'wallet/home.html'
    return render(request, template, {})

def account(request):
    template = 'wallet/account.html'
    return render(request, template, {})

def dashboard(request):
    template = 'wallet/dashboard.html'
    return render(request, template, {})

def wallet(request):
    template = 'wallet/wallet.html'
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

def activate(request):
    template = 'wallet/activate.html'
    horizon_url = settings.HORIZON_LIVE
    server = Server(horizon_url)
    media_dir = './media/'

    # Create media folder if not available: We will store wallet qr-codes during user session
    try:
        os.mkdir(media_dir)
    except FileExistsError:
        print("Directory ", media_dir,  " already exists")

    # Get user secret
    secret = request.POST.get('secret', '')
    # Generate keypair from secret
    new_account = Keypair.from_secret(secret)
    # Begin account activation.
    public_key = new_account.public_key

    # Generate the wallet QR Code image and location
    QRurl = media_dir + public_key + ".png"
    qr_from_key(public_key, media_dir)

    # Load required variables into template
    instruct_context = {
        'public_key': public_key,
        'qr': QRurl
    }

    # Check if the new account exists on the stellar network convert response to json string and parse
    account = requests.get(account_url + public_key, data={})
    data = account.json()
    try:
        data['id']
    except KeyError:
        # Inactive Account:
        # It has to funded with the minimum balance of 5 XML before activation.
        # Generate QR code and deposit instructions
        return render(request, template, instruct_context)
    else:
        # Active Account
        # Store some variables in the session
        request.session['wallet_id'] = data['id']
        request.session['transactions_url'] = string_cleaner( data['_links']['transactions']['href'])
        request.session['operations_url'] = string_cleaner(data['_links']['operations']['href'])
        request.session['payments_url'] = string_cleaner(data['_links']['payments']['href'])
        request.session['effects_url'] = string_cleaner(data['_links']['effects']['href'])
        request.session['offers_url'] = string_cleaner(data['_links']['offers']['href'])
        request.session['trades_url'] = string_cleaner(data['_links']['trades']['href'])
        request.session['data_url'] = string_cleaner(data['_links']['data']['href'])
        # Custom content rewiting
        for asset in data['balances']:
            if asset['asset_type'] == 'native':
                asset['asset_code'] = 'XLM'

        # Send some more variables to the session
        data_context = {
            'id': data['id'],
            'qr': '.' + QRurl,
            'last_modified': data['last_modified_time'],
            'balances': data['balances']
        }
        request.session['session_data'] = data_context
        # All good! This is an active wallet. Free to manage
        return redirect('/dashboard/')

################# HELPERS #########################

def qr_from_key(key, location):
    img = qrcode.make(key)
    type(img)  # qrcode.image.pil.PilImage
    img.save(location + key + ".png")

def string_cleaner(string):
    clean = string.replace('{', '')
    string = clean.replace('}', '')
    return string
