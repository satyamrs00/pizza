import json
from django.db.utils import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from itertools import chain
from django.contrib.auth.decorators import login_required
import operator
import decimal
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist

from orders.forms import Addressform, RegistrationForm, LoginForm
from orders.models import Addon, PizzaCombination, Sub, Topping, User, Pizza, Pasta, Salad, Platter, Cart, SubCombination, PlatterCombination, CartPizza, CartSub, CartPasta, CartSalad, CartPlatter, WeightedM2M, OrderPizza, OrderSub, OrderPasta, OrderSalad, OrderPlatter, Address, Order
from pizza.settings import DEFAULT_FROM_EMAIL

THINGS=["pizza", "sub", "pasta", "salad", "platter"]

# Create your views here.
def index(request):
    try:
        c = Cart.objects.get(user=request.user)
        request.session['cartcount'] = len(list(chain.from_iterable(getattr(c, 'cart'+thing+'_set').all() for thing in THINGS)))
    except:
        request.session['cartcount'] = 0

    return render(request, "orders/index.html")

def menu(request):
    rpizzas = Pizza.objects.filter(type=0).order_by('id')
    spizzas = Pizza.objects.filter(type=1).order_by('id')
    subs = Sub.objects.all().order_by('id')
    pastas = Pasta.objects.all().order_by('id')
    salads = Salad.objects.all().order_by('id')
    platters = Platter.objects.all().order_by('id')
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
        form = json.loads(request.body)
        try:
            if form['password1'] != form['password2']:
                return JsonResponse({
                    "success": False,
                    "msg" : "Passwords do not match !!!"
                })

            u = User(username = form['username'])
            u.set_password(form['password1'])
            u.first_name = form['first_name'].capitalize()
            if form['last_name']:
                u.last_name = form['last_name'].capitalize()
            u.email = form['email']
            u.save()
            
            subject = "Pizza - Registration successful"
            message = "Thank you for registering at Pinochhio's Pizza. Your account is currently active and you can view your profile here https://pinopizza.herokuapp.com/account"
            send_mail(subject=subject, message=message, from_email=DEFAULT_FROM_EMAIL, recipient_list=[form['email']], fail_silently=True)

            login(request, u)

            return JsonResponse({
                "success": True
            })
        except IntegrityError:
            return JsonResponse({
                "success": False,
                'msg' : 'Username already exists !!!'
            })

    return render(request, 'orders/register.html', {
        'form': RegistrationForm
    })

def login_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return JsonResponse({"success": True})
            # return redirect('index')
        else:
            return JsonResponse({"success": False})
            # return HttpResponse('username and password do not match')

    return render(request, "orders/login.html", {
        "form": LoginForm
    })

def logout_view(request):
    if request.user is not None:
        logout(request)
    
    return redirect('index')

def item(request, thing, id):
    if request.method == "PUT":
        """repeat the same item"""
        c = Cart.objects.get(user=request.user)

        if thing in ['PizzaCombination', 'SubCombination', 'PlatterCombination']:
            thing = thing[:-11]

        thingcartrel = "Cart" + thing
        thingcartrel = globals()[thingcartrel]

        for item in thingcartrel.objects.filter(cart=c):
            if getattr(item, thing.lower()).id == id:
                r = item

        r.quantity += 1
        r.save()

        c.price += getattr(r, thing.lower()).price
        c.save()

        request.session['cartcount'] += 1

        return JsonResponse({
            "success" : "added to cart"
        })

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

        c.price -= decimal.Decimal(i.price)
        c.save()

        request.session['cartcount'] -= 1

        return JsonResponse({
            "message": "successfully removed"
        })

    cthing = thing.capitalize()
    try:
        thingcls = globals()[cthing]        
    except KeyError:
        return render(request, "orders/404.html")

    if request.method == "POST":
        """add the item to cart"""

        if thing in ['pizza', 'sub', 'platter']:
            if not request.POST.get('size'):
                return HttpResponse('Select Size')

        if thing == 'pizza':
            if len(request.POST.getlist('Toppings')) != thingcls.objects.get(id=id).extrascount:
                return HttpResponse('Select proper number of toppings')
                
            try:
                # this if statement is to tackle bug2
                if thingcls.objects.get(id=id).extrascount == 0:
                    p = PizzaCombination.objects.filter(pizza=thingcls.objects.get(id=id), size=request.POST.get('size'))[0]
                else:
                    p = PizzaCombination.objects.filter(pizza=thingcls.objects.get(id=id), size=request.POST.get('size'), toppings__in= [int(e[8:]) for e in request.POST.getlist('Toppings')])[0]
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
        except TypeError:
            return render(request, 'orders/login.html', {
                'form': LoginForm,
                'msg': 'You need to login to add items to cart'
            })

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

        c.price += decimal.Decimal(p.price)
        c.save()

        try:
            request.session['cartcount'] += 1
        except KeyError:
            cartcount = 0
            itemrels = list(chain.from_iterable(getattr(c, 'cart'+thing+'_set').all() for thing in THINGS))
            for item in itemrels:
                cartcount += item.quantity
            request.session['cartcount'] = cartcount

        return redirect('menu')

    """get information about the item to load the form to add to cart"""
    try:
        p = thingcls.objects.get(id=id)
    except ObjectDoesNotExist:
        return render(request, 'orders/404.html')

    try:
        p.smallprice
        missingsize = None
        sizeoptions = True
        if p.smallprice == 0.00:
            missingsize = "small"
        if p.largeprice == 0.00:
            missingsize = "large"
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
            "missingsize": missingsize,
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
            "missingsize": missingsize,
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

def placed(request):
    return render(request, 'orders/order_placed.html')

@login_required
def cart(request):
    try:
        c = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        c = Cart(user=request.user)
        c.save()

    if request.method == "POST":

        """place order"""
        data = request.POST
        if not data.get('address'):
            return render(request, "orders/index.html", {
                "error": "Address not selected"
            })
            
        if not data.get('paymethod') or data.get("paymethod") == "":
            return render(request, "orders/index.html", {
                "error": "Payment method not selected"
            })

        if data.get('address') == "addaddress":
            form = Addressform(request.POST)
            if form.is_valid():
                form = form.cleaned_data
                a = Address(name=form['name'], addressline=form['addressline'], city=form['city'], state=form['state'], country=form['country'], pin=form['pin'], phone=form['phone'], user=request.user)
                a.save()
        else:
            a = Address.objects.get(id=data.get('address')[7:])

        o = Order(user=request.user, payment_mode=data.get('paymethod'), address=a, price=c.price)
        o.save()

        for thing in THINGS:
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
        
        request.session['cartcount'] = 0
        subject = "Pizza - Order Confirmation"
        message = "Thank you for ordering from Pinochhio's Pizza. Your order is currently being prepared and will be delivered to you within 40 minutes"
        send_mail(subject=subject, message=message, from_email=DEFAULT_FROM_EMAIL, recipient_list=[request.user.email], fail_silently=True)
        return redirect('placed')
    
    """load cart details"""
    items = []
    quantities = []
    itemrels = list(chain.from_iterable(getattr(c, 'cart'+thing+'_set').all() for thing in THINGS))
    itemrels = sorted(itemrels, key=operator.attrgetter('datetime_added'), reverse=True)
    for item in itemrels:
        items.append(getattr(item, item.__class__.__name__.lower()[4:]))
        quantities.append(item.quantity)

    addresses = Address.objects.filter(user=request.user)

    return render(request, 'orders/cart.html', {
        "items": list(zip(items, quantities)),
        "cart": c,
        "addresses" : addresses,
        "form": Addressform
    })

@login_required
def orders(request):
    """show all orders in breif"""
    orders = Order.objects.filter(user=request.user).order_by('-placedtime')
    allitems = []
    for o in orders:
        items = []
        quantities = []
        for item in list(chain.from_iterable(getattr(o, 'order'+thing+'_set').all() for thing in THINGS)):
            items.append(getattr(item, item.__class__.__name__.lower()[5:]))
            quantities.append(item.quantity)
        items = list(zip(items, quantities))
        allitems.append(items)
    
    return render(request, 'orders/orders.html', {
        "allitems": list(zip(allitems, orders))
    })

@login_required
def order(request, order_id):
    if request.method == 'POST':
        """repeat order"""
        data = request.POST
        if not data.get('address'):
            return HttpResponse('select address')
        
        if not data.get('paymethod') or data.get("paymethod") == "":
            return HttpResponse('select payment method')

        if data.get('address') == "addaddress":
            form = Addressform(request.POST)
            if form.is_valid():
                form = form.cleaned_data
                a = Address(name=form['name'], addressline=form['addressline'], city=form['city'], state=form['state'], country=form['country'], pin=form['pin'], phone=form['phone'], user=request.user)
                a.save()
        else:
            a = Address.objects.get(id=data.get('address')[7:])
            
        o1 = Order.objects.get(id=order_id)
        o2 = Order(user=request.user, payment_mode=data.get('paymethod'), address=a, price=o1.price)
        o2.save()
        for thing in THINGS:
            orders = "Order" + thing.capitalize()
            orderc = globals()[orders]

            oo1 = orderc.objects.filter(order=o1)
            for oneoo in oo1:
                oo2 = orderc(order=o2)
                setattr(oo2, thing, getattr(oneoo, thing))
                oo2.save()
                oo2.quantity = oneoo.quantity
                oo2.save()

        subject = "Pizza - Order Confirmation"
        message = "Thank you for ordering from Pinochhio's Pizza. Your order is currently being prepared and will be delivered to you within 40 minutes"
        send_mail(subject=subject, message=message, from_email=DEFAULT_FROM_EMAIL, recipient_list=[request.user.email], fail_silently=True)
        return redirect('placed')


    """show details of one order"""
    try:
        o = Order.objects.get(id=order_id)
    except ObjectDoesNotExist:
        return render(request, 'orders/order.html')

    items = []
    quantities = []
    itemrels = list(chain.from_iterable(getattr(o, 'order'+thing+'_set').all() for thing in THINGS))
    itemrels = sorted(itemrels, key=operator.attrgetter('datetime_added'), reverse=True)
    addresses = Address.objects.filter(user=request.user)

    for item in itemrels:
        items.append(getattr(item, item.__class__.__name__.lower()[5:]))
        quantities.append(item.quantity)

    return render(request, "orders/order.html", {
        "o" : o,
        "items": list(zip(items, quantities)),
        'addresses' : addresses,
        'form': Addressform
    })

@login_required
def my_account(request):
    if request.method == 'DELETE':
        """delete address"""

        data = json.loads(request.body)
        a = Address.objects.get(id=int(data.get('id')))
        a.user = None
        a.save()
        print(data)

        return JsonResponse({
            "success": True
        })

    if request.method == "PUT":
        """edit address"""

        data = json.loads(request.body)
        a = Address.objects.get(id=data.get('id'))
        for item in data:
            setattr(a, item, data.get(item))
        a.save()

        return JsonResponse({
            'success': True
        })

    if request.method == "PATCH":
        """update account details"""

        data = json.loads(request.body)
        if len(User.objects.filter(username=data['username'])) != 0 and User.objects.get(username=data['username']) != request.user:
            return JsonResponse({
                "success": False,
                "error": "Username already exists !!!"
            })

        u = request.user
        for item in data:
            setattr(u, item, data.get(item))
        u.save()

        return JsonResponse({
            "success": True
        })

    if request.method == "POST":
        """add address"""
        form = Addressform(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            a = Address(name=form['name'], addressline=form['addressline'], city=form['city'], state=form['state'], country=form['country'], pin=form['pin'], phone=form['phone'], user=request.user)
            a.save()
            return redirect('my_account')

    """show account details and addresses"""
    addresses = Address.objects.filter(user=request.user).order_by("-id")
    return render(request, "orders/my_account.html",{
        "addresses": addresses,
        "form": Addressform
    })

@login_required
def address(request, id):
    """return address details"""
    try:
        a = Address.objects.get(id=id)
    except ObjectDoesNotExist:
        return render(request, 'orders/404.html')
    return JsonResponse({
        'id': a.id,
        'name': a.name,
        'addressline': a.addressline,
        'city': a.city,
        'state': a.state,
        'country': a.country,
        'pin': a.pin,
        'phone': str(a.phone)
    })