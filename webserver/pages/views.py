from django.shortcuts import render
from django.http import HttpResponse

def index(req):
    context = {}
    return render(req, 'pages/index.html', context)
