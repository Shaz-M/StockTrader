from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm
from portfolio.models import Portfolio

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            newPortfolio = Portfolio(initialBalance=0,cashBalance=0,user=user)
            newPortfolio.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Your account has been created! You are now able to log in')
            return redirect('portfolio:dashboard')
    else:
        form = UserRegisterForm()
    return render(request,'users/register.html',{'form':form})
