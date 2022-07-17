from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt

from orders.forms import RegistrationForm, LoginForm
from orders.models import Addon, Sub, Topping, User, Pizza, Pasta, Salad, Platter

# Create your views here.
def index(request):
    rpizzas = Pizza.objects.filter(type=0)
    spizzas = Pizza.objects.filter(type=1)
    toppings = Topping.objects.all()
    subs = Sub.objects.all()
    addons = Addon.objects.all()
    pastas = Pasta.objects.all()
    salads = Salad.objects.all()
    platters = Platter.objects.all()
    return render(request, 'orders/index.html', {
        "rpizzas": rpizzas,
        "spizzas": spizzas,
        "toppings": toppings,
        "subs": subs,
        "addons": addons,
        "pastas": pastas,
        "salads": salads,
        "platters": platters,    
    })

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

@csrf_exempt
def item(request, thing, id):
    thing = thing.capitalize()
    thing = globals()[thing]        
    p = thing.objects.get(id=id)

    try:
        p.smallprice
        sizeoptions = True
    except AttributeError:
        sizeoptions = False
    
    extrasoption = False
    if thing == Pizza or thing == Sub:
        extrasoption = True
        if thing == Pizza:
            t = Topping.objects.all()
            extrasamount = p.extrascount
            extrastype = 'Toppings'
        else:
            t = Addon.objects.all()
            extrastype = 'Add-ons'
            extrasamount = Addon.objects.count()

        extras = []
        extrasname = []
        extrasprice = []
        for item in t:
            extras.append(item.id)
            extrasname.append(item.name)
            extrasprice.append(item.price)

        return JsonResponse({
            "id": p.id,
            "name": p.name,
            "sizeoptions": sizeoptions,
            "extrasoption": extrasoption,
            "smallprice": p.smallprice,
            "largeprice": p.largeprice,
            "extras": extras,
            "extrasname": extrasname,
            "extrasprice": extrasprice,
            "extrastype": extrastype,
            "extrasamount": extrasamount
        })

    if extrasoption == False and sizeoptions == True:
        return JsonResponse({
            "id": p.id,
            "name": p.name,
            "sizeoptions": sizeoptions,
            "extrasoption": extrasoption,
            "smallprice": p.smallprice,
            "largeprice": p.largeprice
        })
    
    if extrasoption == False and sizeoptions == False:
        return JsonResponse({
            "id": p.id,
            "name": p.name,
            "sizeoptions": sizeoptions,
            "extrasoption": extrasoption,
            "price": p.price
        })
