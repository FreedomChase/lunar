from django.shortcuts import render
from django.http import HttpResponse
from stellar_sdk.keypair import Keypair
from stellar_sdk import Server, exceptions
from django.conf import settings
import qrcode
import os
import requests

account_url = settings.HORIZON_LIVE + '/accounts/'


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
    template = 'wallet/activate.html'
    horizon_url = settings.HORIZON_LIVE
    server = Server(horizon_url)
    media_dir = 'media/'

    try:
        # Create media folder if not available: We will store wallet qr-codes during user session
        os.mkdir(media_dir)
    except FileExistsError:
        print("Directory ", media_dir,  " already exists")

    # Get user secret
    secret = request.POST.get('secret', '')
    # Generate keypair from secret
    new_account = Keypair.from_secret(secret)
    # Begin account activation.
    public_key = new_account.public_key
    # Check if the new account exists on the stellar network.

    try:
        # Active Account: get data
        account = requests.get(account_url + public_key, data={})
        data = account.json()

        # Store some variables in the session
        request.session['wallet_id'] = data['id']
        request.session['transactions_url'] = string_cleaner(
            data['_links']['transactions']['href'])
        request.session['operations_url'] = string_cleaner(
            data['_links']['operations']['href'])
        request.session['payments_url'] = string_cleaner(
            data['_links']['payments']['href'])
        request.session['effects_url'] = string_cleaner(
            data['_links']['effects']['href'])
        request.session['offers_url'] = string_cleaner(
            data['_links']['offers']['href'])
        request.session['trades_url'] = string_cleaner(
            data['_links']['trades']['href'])
        request.session['data_url'] = string_cleaner(
            data['_links']['data']['href'])

        data_context = {
            'id': data['id'],
            'last_modified': data['last_modified_time'],
            'balances': data['balances']
        }
        template = 'wallet/dashboard.html'
        return render(request, template, data_context)
    except exceptions.NotFoundError:
        # Inactive Account
        # It has to funded with the minimum balance of 5 XML before activation.
        # Generate QR code and deposit instructions
        img = qrcode.make(public_key)
        type(img)  # qrcode.image.pil.PilImage
        img.save(media_dir + public_key + ".png")

    QRurl = '../' + media_dir + public_key + ".png"
    # Load required variables into template
    instruct_context = {
        'public_key': public_key,
        'qr': QRurl
    }
    return render(request, template, instruct_context)


def string_cleaner(string):
    clean = string.replace('{', '')
    string = clean.replace('}', '')
    return string
