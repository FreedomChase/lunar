from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    template = 'wallet/index.html'
    return render(request, template, {})
