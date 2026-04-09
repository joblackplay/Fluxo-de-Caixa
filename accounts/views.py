from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from .models import Account
from .forms import SignUpForm

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = Account.objects.create_user(first_name=first_name,last_name=last_name,username = username, password = password)
            login(request, user)
            redirect('accounts/register.html')
    else:   
        form = SignUpForm()
        return render(request, 'accounts/register.html',{'form': form})
    
    return render(request, 'register.html',{'form': form})