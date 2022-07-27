import json
import re
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
import decimal
from itertools import chain
from django.contrib.auth.decorators import login_required

from orders.forms import RegistrationForm, LoginForm
from orders.models import Addon, PizzaCombination, Sub, Topping, User, Pizza, Pasta, Salad, Platter, Cart, SubCombination, PlatterCombination, CartPizza, CartSub, CartPasta, CartSalad, CartPlatter, WeightedM2M, OrderPizza, OrderSub, OrderPasta, OrderSalad, OrderPlatter, Address, Order

# Create your views here.
def index(request):
    return render(request, "orders/index.html")

def menu(request):
    rpizzas = Pizza.objects.filter(type=0)
    spizzas = Pizza.objects.filter(type=1)
    subs = Sub.objects.all()
    pastas = Pasta.objects.all()
    salads = Salad.objects.all()
    platters = Platter.objects.all()
    return render(request, 'orders/menu.html', {
        "rpizzas": rpizzas,
        "spizzas": spizzas,
        "subs": subs,
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
        """remove the item from cart"""

        thingcls = globals()[thing]
        i = thingcls.objects.get(id=id)
        if thing in ['PizzaCombination', 'SubCombination', 'PlatterCombination']:
            thing = thing[:-11]

        c = Cart.objects.get(user=request.user)
        
        thingcartrel = "Cart" + thing
        thingcartrel = globals()[thingcartrel]            
        
        for item in thingcartrel.objects.filter(cart=c):
            if getattr(item, thing.lower()) == i:
                r = item
        
        if r.quantity > 1:
            r.quantity -= 1
            r.save()
        else:
            r.delete()

        c.price -= i.price
        c.save()
        return JsonResponse({
            "message": "successfully removed"
        })

    cthing = thing.capitalize()
    thingcls = globals()[cthing]        

    if request.method == "POST":
        """add the item to cart"""

        if thing in ['pizza', 'sub', 'platter']:
            if not request.POST.get('size'):
                return HttpResponse('Select Size')

        if thing == 'pizza':
            if len(request.POST.getlist('Toppings')) != thingcls.objects.get(id=id).extrascount:
                print(len(request.POST.get('Toppings')))
                print(thingcls.objects.get(id=id).extrascount)
                return HttpResponse('Select proper number of toppings')
                
            try:
                print(request.POST.getlist('Toppings'))
                print([int(e[8:]) for e in request.POST.getlist('Toppings')])

                # this if statement is to tackle bug2
                if thingcls.objects.get(id=id).extrascount == 0:
                    p = PizzaCombination.objects.filter(pizza=thingcls.objects.get(id=id), size=request.POST.get('size'))[0]
                else:
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
                # this if statement is to tackle bug2
                if request.POST.get('Add-ons') == []:
                    p = SubCombination.objects.filter(sub=thingcls.objects.get(id=id), size=request.POST.get('size'))
                else:
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

        thingcartrel = "Cart" + cthing
        thingcartrel = globals()[thingcartrel]
        
        try:
            r = None
            for item in thingcartrel.objects.filter(cart = c):
                if getattr(item, thing) == p:
                    r = item
            if not r:
                r = thingcartrel(cart=c)
                setattr(r, thing, p)
                r.save()                 
        except:
            r = thingcartrel(cart=c)
            setattr(r, thing, p)
            r.save() 

        r.quantity +=1
        r.save()

        c.price += p.price
        c.save()
        return redirect('menu')

    """get information about the item to load the form to add to cart"""
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
            if p.extrascount == 0:
                extrasoption = False

        else:
            t = Addon.objects.all()
            extrastype = 'Add-ons'
            extrasamount = Addon.objects.count()

        extras = []
        for item in t:
            extras.append({
                "id" : item.id,
                "name" : item.name,
                "price" : item.price
            })

        return JsonResponse({
            "id": p.id,
            "name": p.getname(),
            "sizeoptions": sizeoptions,
            "extrasoption": extrasoption,
            "smallprice": p.smallprice,
            "largeprice": p.largeprice,
            "extras": extras,
            "extrastype": extrastype,
            "extrasamount": extrasamount
        })

    if extrasoption == False and sizeoptions == True:
        return JsonResponse({
            "id": p.id,
            "name": p.getname(),
            "sizeoptions": sizeoptions,
            "extrasoption": extrasoption,
            "smallprice": p.smallprice,
            "largeprice": p.largeprice
        })
    
    if extrasoption == False and sizeoptions == False:
        return JsonResponse({
            "id": p.id,
            "name": p.getname(),
            "sizeoptions": sizeoptions,
            "extrasoption": extrasoption,
            "price": p.price
        })

@login_required
def cart(request):
    c = Cart.objects.get(user=request.user)
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        if not data.get('address') or data.get("address") == "":
            return JsonResponse({
                "error": "No address provided"
            })
        if not data.get('paymethod') or data.get("paymethod") == "":
            return JsonResponse({
                "error": "Payment method not selected"
            })

        a = Address(address=data.get('address'), user = request.user)
        a.save()

        o = Order(user=request.user, payment_mode=data.get('paymethod'), address=a, price=c.price)
        o.save()

        things=["pizza", "sub", "pasta", "salad", "platter"]

        for thing in things:
            carts = "Cart" + thing.capitalize()
            cartc = globals()[carts]
            orders = "Order" + thing.capitalize()
            orderc = globals()[orders]
            
            co = cartc.objects.filter(cart=c)
            for oneco in co:
                oo = orderc(order=o)
                setattr(oo, thing, getattr(oneco, thing))
                oo.save()
                oo.quantity = oneco.quantity
                oo.save()
                oneco.delete()
                c.price = 0
                c.save()
        
        return JsonResponse({
            "success": "order placed",
            "redirect": "/"
        })
    if request.method == "PUT":
        return JsonResponse({
            "id": c.id,
            "price": c.price
        })
    
    items = list(chain(c.pizza.all(), c.sub.all(), c.pasta.all(), c.salad.all(), c.platter.all()))
    quantities = []
    for item in list(chain(c.cartpizza_set.all(), c.cartsub_set.all(), c.cartpasta_set.all(), c.cartsalad_set.all(), c.cartplatter_set.all())):
        quantities.append(item.quantity)
    return render(request, 'orders/cart.html', {
        "items": list(zip(items, quantities)),
        "cart": c
    })

def orders(request):
    orders = Order.objects.filter(user=request.user)
    allitems = []
    for o in orders:
        items = list(chain(o.pizza.all(), o.sub.all(), o.pasta.all(), o.salad.all(), o.platter.all()))
        quantities = []
        for item in list(chain(o.orderpizza_set.all(), o.ordersub_set.all(), o.orderpasta_set.all(), o.ordersalad_set.all(), o.orderplatter_set.all())):
            quantities.append(item.quantity)
        items = list(zip(items, quantities))
        allitems.append(items)
    
    return render(request, 'orders/orders.html', {
        "allitems": list(zip(allitems, orders))
    })

def order(request, order_id):
    o = Order.objects.get(id=order_id)
    items = list(chain(o.pizza.all(), o.sub.all(), o.pasta.all(), o.salad.all(), o.platter.all()))
    quantities = []
    for item in list(chain(o.orderpizza_set.all(), o.ordersub_set.all(), o.orderpasta_set.all(), o.ordersalad_set.all(), o.orderplatter_set.all())):
        quantities.append(item.quantity)

    return render(request, "orders/order.html", {
        "o" : o,
        "items": list(zip(items, quantities))
    })