from django.shortcuts import render
from .forms import TickerForm
from django.http import HttpResponseRedirect

# Create your views here.


def dashboard(request):
    if(request.method == 'POST'):
        form = TickerForm(request.POST)
        if form.is_valid():
            ticker = request.POST['ticker']
            return HttpResponseRedirect('stocks/'+ticker)
    else:
        form = TickerForm();    
    context = {'form':form}
    return render(request,'portfolio/dashboard.html',context)

def positions(request):
    return render(request,'portfolio/positions.html')