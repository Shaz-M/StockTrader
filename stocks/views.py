from urllib import response
from wsgiref.util import request_uri
from django.shortcuts import render
from .forms import TickerForm
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
import requests
import json;

# Create your views here.
def index(request):
    if(request.method == 'POST'):
        form = TickerForm(request.POST)
        if form.is_valid():
            ticker = request.POST['ticker']
            return HttpResponseRedirect(ticker)
    else:
        form = TickerForm();    
    context = {'form':form}
    return render(request,'stocks/index.html',context)


def ticker(request,tid):
    tid = tid.upper()
    context = {'ticker':tid}
    url = 'https://api.tdameritrade.com/v1/marketdata/'+tid+'/quotes?apikey=D57TGYGPEEXE5IQRTHZG4EVDBATABE3B'
    response = requests.get(url)
    response  = response.json()
    if not response:
        return redirect('dashboard')
    return render(request,'stocks/ticker.html',context)