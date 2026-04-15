from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required(login_url = 'login')
def home(request):
    return render(request,'home.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request,username=username,password=password)
        print(user)
        if user is not None:
            login(request,user)
            
            return redirect('home')
        else:
            messages.success(request,"Ocorreu um erro ao efetuar o login. Por favor, tente novamente.")
            return redirect('login')
    else:    
        return render(request,'login.html')
    
def logout_user(request):
    logout(request)
    messages.success(request, "You Have Been Logged Out...")
    return redirect('home')
