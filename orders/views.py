from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
import decimal
from django.core.exceptions import ObjectDoesNotExist

from orders.forms import RegistrationForm, LoginForm
from orders.models import Addon, PizzaCombination, Sub, Topping, User, Pizza, Pasta, Salad, Platter, Cart, SubCombination

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
    thingcls = thing.capitalize()
    thingcls = globals()[thingcls]        

    if request.method == "POST":
        if thing in ['pizza', 'sub', 'platter']:
            if not request.POST.get('size'):
                return HttpResponse('Select Size')

        price = 0

        if thing == 'pizza':
            if len(request.POST.get('Toppings')) != thingcls.objects.get(id=id).extrascount:
                return HttpResponse('Select proper number of toppings')
                
            try:
                p = PizzaCombination.objects.filter(pizza=thingcls.objects.get(id=id), toppings__in= [int(e[8:]) for e in request.POST.getlist('Toppings')])[0]
                print(p)
            except IndexError:
                p = PizzaCombination(pizza=thingcls.objects.get(id=id))
                p.save()

                p.smallprice = thingcls.objects.get(id=id).smallprice
                p.largeprice = thingcls.objects.get(id=id).largeprice
                
                for topping in request.POST.getlist('Toppings'):
                    topping_id = int(topping[8:])
                    p.toppings.add(Topping.objects.get(id=topping_id))
                    p.smallprice += Topping.objects.get(id=topping_id).price
                    p.largeprice += Topping.objects.get(id=topping_id).price
                p.save()

        if thing == 'sub':
            try:
                p = SubCombination.objects.filter(sub=thingcls.objects.get(id=id), addons__in= [int(e[7:]) for e in request.POST.getlist('Add-ons')])[0]
                print(p)
            except IndexError:
                p = SubCombination(sub=thingcls.objects.get(id=id))
                p.save()

                p.smallprice = thingcls.objects.get(id=id).smallprice
                p.largeprice = thingcls.objects.get(id=id).largeprice
                
                for addon in request.POST.getlist('Add-ons'):
                    addon_id = int(addon[7:])
                    p.addons.add(Addon.objects.get(id=addon_id))
                    p.smallprice += Addon.objects.get(id=addon_id).price
                    p.largeprice += Addon.objects.get(id=addon_id).price
                p.save()

        p = thingcls.objects.get(id=id)
        if request.POST.get('size') == 'small':
            price = p.smallprice
        elif request.POST.get('size') == 'large':
            price = p.largeprice
        else:
            price = p.price
        print(price)

        try:
            c = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            c = Cart(user=request.user)
            c.save()

        if thing == 'pizza':
            c.pizza.add(p)
        elif thing == 'sub':
            c.sub.add(p)
        if thing == 'pasta':
            c.pasta.add(p)
        elif thing == 'salad':
            c.salad.add(p)
        elif thing == 'platter':
            c.platter.add(p)

        c.price += decimal.Decimal(price)
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
