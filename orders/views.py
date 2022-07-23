import re
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
import decimal
from itertools import chain

from orders.forms import RegistrationForm, LoginForm
from orders.models import Addon, PizzaCombination, Sub, Topping, User, Pizza, Pasta, Salad, Platter, Cart, SubCombination, PlatterCombination

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

def item(request, thing, id):
    if request.method == "PATCH":
        thingcls = globals()[thing]
        print(thingcls)
        i = thingcls.objects.get(id=id)
        print(thing)
        if thing in ['PizzaCombination', 'SubCombination', 'PlatterCombination']:
            thing = thing[:-11]
            print(thing)

        c = Cart.objects.get(user=request.user)
        getattr(c, thing.lower()).remove(i)
        c.price -= i.price
        c.save()
        return JsonResponse({
            "message": "successfully removed"
        })

    thingcls = thing.capitalize()
    thingcls = globals()[thingcls]        

    if request.method == "POST":
        if thing in ['pizza', 'sub', 'platter']:
            if not request.POST.get('size'):
                return HttpResponse('Select Size')

        if thing == 'pizza':
            if len(request.POST.getlist('Toppings')) != thingcls.objects.get(id=id).extrascount:
                print(len(request.POST.get('Toppings')))
                print(thingcls.objects.get(id=id).extrascount)
                return HttpResponse('Select proper number of toppings')
                
            try:
                p = PizzaCombination.objects.filter(pizza=thingcls.objects.get(id=id), size=request.POST.get('size'), toppings__in= [int(e[8:]) for e in request.POST.getlist('Toppings')])[0]
                print(p)
            except IndexError:
                p = PizzaCombination(pizza=thingcls.objects.get(id=id), size=request.POST.get('size'))
                p.save()

                if request.POST.get('size') == "small":
                    p.price = thingcls.objects.get(id=id).smallprice
                elif request.POST.get('size') == "large":
                    p.price = thingcls.objects.get(id=id).largeprice
                
                for topping in request.POST.getlist('Toppings'):
                    topping_id = int(topping[8:])
                    p.toppings.add(Topping.objects.get(id=topping_id))
                    p.price += Topping.objects.get(id=topping_id).price
                p.save()

        elif thing == 'sub':
            try:
                p = SubCombination.objects.filter(sub=thingcls.objects.get(id=id), size=request.POST.get('size'), addons__in= [int(e[7:]) for e in request.POST.getlist('Add-ons')])[0]
                print(p)
            except IndexError:
                p = SubCombination(sub=thingcls.objects.get(id=id), size=request.POST.get('size'))
                p.save()

                if request.POST.get('size') == "small":
                    p.price = thingcls.objects.get(id=id).smallprice
                elif request.POST.get('size') == "large":
                    p.price = thingcls.objects.get(id=id).largeprice
                
                for addon in request.POST.getlist('Add-ons'):
                    addon_id = int(addon[7:])
                    p.addons.add(Addon.objects.get(id=addon_id))
                    p.price += Addon.objects.get(id=addon_id).price
                p.save()

        elif thing == "platter":
            try:
                p = PlatterCombination.objects.filter(platter=thingcls.objects.get(id=id), size=request.POST.get('size'))[0]
                print(p)
            except IndexError:
                p = PlatterCombination(platter=thingcls.objects.get(id=id), size=request.POST.get('size'))
                p.save()

                if request.POST.get('size') == "small":
                    p.price = thingcls.objects.get(id=id).smallprice
                elif request.POST.get('size') == "large":
                    p.price = thingcls.objects.get(id=id).largeprice
           
                p.save()
            
        else:
            p = thingcls.objects.get(id=id)
        
        try:
            c = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            c = Cart(user=request.user)
            c.save()

        getattr(c, thing).add(p)

        c.price += p.price
        c.save()
        return redirect('index')

    p = thingcls.objects.get(id=id)

    try:
        p.smallprice
        sizeoptions = True
    except AttributeError:
        sizeoptions = False
    
    extrasoption = False
    if thingcls == Pizza or thingcls == Sub:
        extrasoption = True
        if thingcls == Pizza:
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

def cart(request):
    c = Cart.objects.get(user=request.user)
    items = list(chain(c.pizza.all(), c.sub.all(), c.pasta.all(), c.salad.all(), c.platter.all()))
    print(c.platter.all())
    print(items)
    return render(request, 'orders/cart.html', {
        "items": items,
        "cart": c
    })