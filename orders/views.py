from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from orders.forms import RegistrationForm, LoginForm
from orders.models import User

# Create your views here.
def index(request):
    
    return render(request, 'orders/index.html')

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            u = User(username = form['username'])
            u.set_password(form['password1'])
            u.first_name = form['first_name']
            u.last_name = form['last_name']
            u.email = form['email']
            u.save()
            login(request, u)

            return redirect('index')
        
        return redirect('register')

    return render(request, 'orders/register.html', {
        'form': RegistrationForm
    })

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        print(username) 
        print(password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print('here')
            login(request,user)
            return redirect('index')
        else:
            return HttpResponse('username and password do not match')

    return render(request, "orders/login.html", {
        "form": LoginForm
    })

def logout_view(request):
    if request.user is not None:
        logout(request)
    
    return redirect('index')