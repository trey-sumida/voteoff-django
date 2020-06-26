from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from .forms import RegisterForm
from .models import Account, AccountDemographics

# Register
def registeracc(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            username_taken = True
            email_taken = True
            try:
                Account.objects.get(username__iexact=username)
            except:
                username_taken = False
            try:
                Account.objects.get(email__iexact=email)
            except:
                email_taken = False
            if username_taken:
                return render(request, 'account/register.html', {'form': form, 'error': 'Username is already taken'})
            elif email_taken:
                return render(request, 'account/register.html', {'form': form, 'error': 'Email is already taken'})
            form.save()
            user = authenticate(request, username=request.POST['username'], password=request.POST['password1'])
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'account/register.html', {'form': form})
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
        try:
            acc = Account.objects.get(email=request.POST['username'])
            user = authenticate(request, username=acc.username, password=request.POST['password'])
        except:
            user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'account/login.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
        else:
            login(request, user)
            return redirect('lists:mycontests', 'all')

def userprofile(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            account = Account.objects.get(pk=request.user.id)
            try:
                account_details = AccountDemographics.objects.get(account=request.user)
            except:
                account_details = AccountDemographics.objects.create(account=request.user)
                account_details.save()
            return render(request, 'account/userprofile.html', {'account': account, 'account_details': account_details})
    else:
        return render(request, 'account/userprofile.html')

def editprofile(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            account = Account.objects.get(pk=request.user.id)
            try:
                account_details = AccountDemographics.objects.get(account=request.user)
            except:
                account_details = AccountDemographics.objects.create(account=request.user)
                account_details.save()
            return render(request, 'account/editprofile.html', {'account': account, 'account_details': account_details})
        else:
            account = Account.objects.get(pk=request.user.id)
            account_details = AccountDemographics.objects.get(account=request.user)
            username_taken = False
            email_taken = False
            try:
                if account.username != request.POST['username']:
                    user = Account.objects.get(username__iexact=request.POST['username'])
                    username_taken = True
            except:
                account.username = request.POST['username']
                account.save()
            try:
                if account.email != request.POST['email']:
                    user = Account.objects.get(email__iexact=request.POST['email'])
                    email_taken = True
            except:
                account.email = request.POST['email']
                account.save()
            account_details.first_name = request.POST['first_name']
            account_details.last_name = request.POST['last_name']
            account_details.save()
            if username_taken:
                return render(request, 'account/editprofile.html', {'error': "username is already taken", 'account': account, 'account_details': account_details})
            elif email_taken:
                return render(request, 'account/editprofile.html', {'error': "Email is already associated with another account", 'account': account, 'account_details': account_details})
            else:
                return redirect('account:userprofile')
    else:
        return render(request, 'account/editprofile.html')