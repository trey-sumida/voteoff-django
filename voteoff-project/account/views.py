from django.shortcuts import render
from .forms import RegisterForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from .models import Account, AccountDemographics

# Register
def registeracc(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(request, username=request.POST['username'], password=request.POST['password1'])
            login(request, user)

            return redirect('index')
        else:
            return render(request, 'account/register.html', {'form': form, 'error': form.errors})
    else:
        form = RegisterForm()
        return render(request, 'account/register.html', {'form': form})

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('index')

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'account/login.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'account/login.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
        else:
            login(request, user)
            return redirect('index')

def userprofile(request):
    if request.method == 'GET':
        account = Account.objects.get(pk=request.user.id)
        account_details = AccountDemographics.objects.get_or_create(account=request.user)
        return render(request, 'account/userprofile.html', {'account': account, 'account_details': account_details})
