from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,logout
# Create your views here.
def Login(request):
    if request.user.is_authenticated:
       return redirect('/') 
    else:
        if request.method =='POST':
            username=request.POST.get('username')
            password=request.POST.get('password')
            user=authenticate(username=username,password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('/')
            else:
                messages.info(request,'Invalid Credentials')
                return redirect('/account/login')
        return render(request,'login.html')

def Register(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method=='POST':
            username=request.POST.get('username')
            email=request.POST.get('email')
            first_name=request.POST.get('first_name')
            last_name=request.POST.get('last_name')
            password=request.POST.get('password')
            vpassword=request.POST.get('vpassword')
            if password==vpassword:
                if User.objects.filter(username=username).exists():
                    messages.info(request,'User already exists')
                    return redirect('/account/register')
                else:
                    user=User.objects.create_user(username=username,email=email,first_name=first_name,last_name=last_name,password=password)
                    user.save()
                    return redirect('/account/login')
            else:
                messages.info(request,'Password Mismatch')
                return redirect('/account/register')
        else:
            return render(request,'register.html')

@login_required
def Logout(request):
    logout(request)
    return redirect('/')