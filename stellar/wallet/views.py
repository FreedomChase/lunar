from django.shortcuts import render
from django.http import HttpResponse
from stellar_sdk.keypair import Keypair


def index(request):
    template = 'wallet/index.html'
    return render(request, template, {})


def create(request):
    template = 'wallet/create.html'
    new_account = Keypair.random()
    context = {
        'public_key' : new_account.public_key,
        'secret' : new_account.secret
    }
    return render(request, template, context)
