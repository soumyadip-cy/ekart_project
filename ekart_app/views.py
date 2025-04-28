from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from ekart_app.models import Categories,Types,Brands,Products,Images,Reviews,ActualStock,TempStock,Carts,Orders,Shipping,Addresses,OrderAddresses,Highlighted_Products
from django.contrib import messages
from ekart_project import settings
from django.db.models import Q
from django.urls import reverse
from urllib.parse import urlencode
from django.http import HttpResponse

prod = Products.objects.all()
prod_imgs = Images.objects.all()
prod_reviews = Reviews.objects.all()
allcat = Categories.objects.all()
alltype = Types.objects.all()
allprod = Products.objects.all()
allTstock = TempStock.objects.all()
allAstock = ActualStock.objects.all()
highlights = Highlighted_Products.objects.all()

def home(request):
    return render(request, 'home.html', {'highlights':highlights,'allstock':allAstock,'prod': prod,'imgs':prod_imgs,'allcat':allcat,'alltype':alltype, 'media_url': settings.MEDIA_URL})

def signup(request):
    return render(request, 'signup.html')

def aboutus(request):
    var=request.GET.get("var")
    return render(request, 'aboutus.html',{'var':var})

def login(request):
    return render(request, 'login.html')

def productpg(request):
    dat = request.GET.get('dat')
    prod = Products.objects.filter(id=dat)
    all_reviews = Reviews.objects.filter(product_fk=dat)
    return render(request, 'product.html', {'allstock':allAstock,'allprod':allprod,'prod': prod,'imgs':prod_imgs,'yrev':all_reviews,'allcat':allcat,'alltype':alltype, 'media_url': settings.MEDIA_URL})

def catpg(request):
    var = request.GET.get('var')
    category = Categories.objects.get(id=var)
    title = category.cat_name
    prod = Types.objects.filter(cat_fk=category)
    return render(request, 'more.html', {'title':title,'var':category,'allstock':allAstock,'allprod':allprod,'prod': prod,'imgs':prod_imgs,'allcat':allcat,'alltype':alltype, 'media_url': settings.MEDIA_URL})

def typpg(request):
    var = request.GET.get('var')
    seltype = Types.objects.get(id=var)
    title = seltype.type_name
    prod = Products.objects.filter(type_fk=seltype)
    return render(request, 'more.html', {'title':title,'var':seltype,'allstock':allAstock,'allprod':allprod,'prod': prod,'imgs':prod_imgs,'allcat':allcat,'alltype':alltype, 'media_url': settings.MEDIA_URL})

def newusr(request):
    if request.method == "POST":
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["email"]
        password = request.POST["password"]
        chk_password = request.POST["chk_password"]
        if chk_password == password:
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Account already exists')
                return redirect('/login')
            else:
                user = User.objects.create_user(
                    first_name=fname, last_name=lname, email=email, username=email, password=password)
                print(user)
                user.save()
                return redirect('/login')
        else:
            return redirect('/')


def logusr(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        if User.objects.filter(email=email).exists() or User.objects.filter(username=email).exists():
            getusr = auth.authenticate(username=email, password=password)
            if getusr is not None:
                auth.login(request, getusr)
                if Carts.objects.filter(user_fk=2).exists():
                   crt = Carts.objects.filter(user_fk=2)
                   for cart in crt:
                        uid = User.objects.get(username=email)
                        if Carts.objects.filter(user_fk=uid,product_fk=cart.product_fk).exists() is False:
                            cart.user_fk = uid
                            cart.save()
                   crt.delete()
                   return redirect('/')
                return redirect('/')
            else:
                messages.error(request, '\n Incorrect password')
                return redirect('/login')
        else:
            messages.error(request, 'Incorrect email')
            return redirect('/login')

def logout(request):
    auth.logout(request)
    return redirect('/')

def srch(request):
    if request.method == "POST":
        name = request.POST["srch"]
        sr = request.POST["typelist"]
        title = "Search Products"
        if Products.objects.filter(name__icontains=name).exists():
            if sr != "all":
                tag = Types.objects.get(id=sr)
                prod = Products.objects.filter(name__icontains=name,type_fk=tag)
            else:
                prod = Products.objects.filter(name__icontains=name)
            title = "Search Result"
            return render(request, 'search.html', {'allstock':allAstock,'title': title, 'prod': prod,'imgs':prod_imgs,'allcat':allcat,'alltype':alltype, 'media_url': settings.MEDIA_URL})

        elif Types.objects.filter(type_name__icontains=name).exists():
            tp = Types.objects.filter(type_name__icontains=name)[0]
            prod = Products.objects.filter(type_fk=tp)
            title = "Items of this Type"
            return render(request, 'search.html', {'allstock':allAstock,'title': title, 'prod': prod,'imgs':prod_imgs,'allcat':allcat,'alltype':alltype, 'media_url': settings.MEDIA_URL})

        elif Brands.objects.filter(brand_name__icontains=name).exists():
            br = Brands.objects.filter(brand_name__icontains=name)[0]
            prod = Products.objects.filter(brand_fk=br)
            title = "Items of this Brand"
            return render(request, 'search.html', {'allstock':allAstock,'title': title, 'prod': prod,'imgs':prod_imgs,'allcat':allcat,'alltype':alltype, 'media_url': settings.MEDIA_URL})

        else:
            messages.error(request, 'Product does not exist')
            return redirect('/')
    else:
        return redirect('/')

def QuantityChange(request):
    if request.method == "POST":
        pid = request.POST["pid"]
        uid = request.POST["uid"]
        if Carts.objects.filter(product_fk=pid,user_fk=uid).exists():
            print("In IF")
            cart = Carts.objects.get(product_fk=pid,user_fk=uid)
            num = request.POST["num"]
            print(num)
            if num=='1':
                if cart.num<=9:
                    cart.num = cart.num+1
            elif num=='3':
                print("Initial")
                cart.num=1
                print(cart.num)
            else:
                if cart.num>1:
                    print("while")
                    cart.num = cart.num-1
                    print(cart.num)
            print(cart.num)
            cart.price = cart.product_fk.price*cart.num
            print(cart.price)
            cart.save()
        else:
            print("In ELSE")
            num = request.POST["num"]
            price = request.POST["price"]
            pid2 = Products.objects.get(id=pid)
            uid2 = User.objects.get(id=uid)
            cart = Carts.objects.create(product_fk=pid2,user_fk=uid2,num=1,price=price)
            cart.save()
        cart = Carts.objects.filter(user_fk=uid)
        frstcrt = Carts.objects.filter(user_fk=uid).first()
        return render(request, 'cart.html', {'frstcrt':frstcrt,'allprod':allprod,'prod': prod,'cart':cart,'imgs':prod_imgs,'allcat':allcat,'alltype':alltype, 'media_url': settings.MEDIA_URL})

def usercart(request):
    uid=request.GET.get('usr')
    cart=Carts.objects.filter(user_fk=uid)
    if cart.exists():
        return render(request, 'cart.html', {'allprod':allprod,'prod':prod, 'cart':cart,'imgs':prod_imgs,'allcat':allcat,'alltype':alltype, 'media_url':settings.MEDIA_URL})
    else:
        empty="yes"
        return render(request, 'cart.html', {'empty':empty,'allprod':allprod,'imgs':prod_imgs,'allcat':allcat,'alltype':alltype, 'media_url':settings.MEDIA_URL})

def buypg(request):
    if request.method == "POST":
        uid = request.POST["uid"]
        pid = request.POST["pid"]
        cart = Carts.objects.create(product_fk=pid,user_fk=uid,num=1,price=Products.objects.filter(id=pid).price)
        cart.save()
    else:
        uid=request.GET.get("buybtn")
        if uid=="2":
            return redirect('/login')
        else:
            cart = Carts.objects.filter(user_fk=uid)
    totprice=0
    for crt in cart:
        totprice=totprice+crt.price
    adrs = Addresses.objects.filter(user_fk=uid)
    return render(request,'buy.html',{'tot':totprice, 'adr':adrs})

def buyfrmcrt(request):
    if request.method == "POST":
        uid=request.POST["buybtn"]
        adrss=request.POST["adrss"]
        crt = Carts.objects.filter(user_fk=uid)
        adrsx = Addresses.objects.get(id=adrss)
        totprice = 0
        if uid=='2':
            return redirect('/login')
        else:
            for cart in crt:
                ords = Orders.objects.create(product_fk=cart.product_fk,user_fk=cart.user_fk,num=cart.num,price=cart.price)
                ords.save()
                stock = ActualStock.objects.get(product_fk=cart.product_fk)
                stock.act_quant = stock.act_quant - cart.num
                stock.save()
                totprice=totprice+cart.price
                ship = Shipping.objects.create(order_id=ords)
                ship.save()
                ordadrs = OrderAddresses.objects.create(order_id=ords,address_id=adrsx)
                ordadrs.save()
            crt.delete()
        page = reverse('userpage')
        userid = urlencode({'uid':uid})
        return redirect('{}?{}'.format(page,userid))

def buydirect(request):
    if request.method == "POST":
        uid = request.POST["uid"]
        pid = request.POST["pid"]
        if uid=='2':
            return redirect('/login')
        else:
            prd = Products.objects.get(id=pid)
            usr = User.objects.get(id=uid)
            if Carts.objects.filter(product_fk=prd,user_fk=usr).exists():
                cart = Carts.objects.get(product_fk=prd,user_fk=usr)
            else:
                cart = Carts.objects.create(product_fk=prd,user_fk=usr,num=1,price=prd.price)
                cart.save()
            adrs = Addresses.objects.filter(user_fk=uid)
            return render(request,'buy.html',{'tot': cart.price, 'adr':adrs})

def delcart(request):
    uid = request.GET.get('delbtn')
    print(uid)
    Carts.objects.filter(user_fk=uid).delete()
    return redirect('/')

def delitem(request):
    if request.method == "POST":
        pid = request.POST["pid"]
        uid = request.POST["uid"]
        crt =  Carts.objects.get(product_fk=pid,user_fk=uid)
        if Carts.objects.filter(product_fk=pid,user_fk=uid).exists():
            crt.delete()
    cart = Carts.objects.filter(user_fk=uid)
    frstcrt = Carts.objects.filter(user_fk=uid).first()
    return render(request, 'cart.html', {'frstcrt':frstcrt,'allprod':allprod,'prod': prod,'cart':cart,'imgs':prod_imgs,'allcat':allcat,'alltype':alltype, 'media_url': settings.MEDIA_URL})

def user_review(request):
    if request.method == "POST":
        uid=request.POST["usrnm"]
        pid=request.POST["prod_id"]
        rev=request.POST["revusr"]
        if Reviews.objects.filter(product_fk=pid, user_fk=uid).exists():
            oldrev = Reviews.objects.get(product_fk=pid,user_fk=uid)
            oldrev.review_text = rev
            oldrev.save()
        else:
            newrev = Reviews.objects.create(review_text=rev,product_fk=Products.objects.get(id=pid),user_fk=User.objects.get(id=uid))
            newrev.save()
    base = reverse('productpg')
    pid = urlencode({'dat':pid})
    return redirect('{}?{}'.format(base,pid))

def delreview(request):
    if request.method == "POST":
        rid=request.POST["rid"]
        pid=Reviews.objects.get(id=rid)
        if Reviews.objects.filter(id=rid).exists():
            delrev = Reviews.objects.get(id=rid)
            delrev.delete()
            messages.success(request,"Review Deleted")
        else:
            messages.error(request,"Could not delete review")
    base = reverse('productpg')
    pid = urlencode({'dat':pid.product_fk.id})
    return redirect('{}?{}'.format(base,pid))

def user_page(request):
    uid = request.GET.get('uid')
    ords = reversed(Orders.objects.filter(user_fk=uid))
    shp_sts = Shipping.objects.all()
    addr = Addresses.objects.filter(user_fk=uid)
    return render(request, 'userpage.html', {'prod': prod,'imgs':prod_imgs,'ords':ords,'shp_sts':shp_sts,'addr':addr,'allcat':allcat,'alltype':alltype, 'media_url': settings.MEDIA_URL})

def deladdr(request):
    addr_id = request.GET.get("addid")
    addr = Addresses.objects.get(id=addr_id)
    uid = addr.user_fk.id
    addr.delete()
    page = reverse('userpage')
    userid = urlencode({'uid':uid})
    return redirect('{}?{}'.format(page,userid))
    
def addaddr(request):
    uid=request.POST["uid"]
    addrs = request.POST["addrs"]
    addr = Addresses.objects.create(user_fk=User.objects.get(id=uid),address=addrs)
    addr.save()
    base = reverse('userpage')
    userid = urlencode({'uid':uid})
    redurl = '{}?{}'.format(base,userid)
    return redirect(redurl)

def changeUserDetails(request):
    if request.method == "POST":
        uid=request.POST["uid"]
        password = request.POST["password"]
        email = request.POST["email"]
        first = request.POST["first"]
        last = request.POST["last"]
        chngpass = request.POST["chngpass"]
        usr = User.objects.get(id=uid)
        print(usr.username)
        if auth.authenticate(username=usr.username,password=password) is not None:
            chng = User.objects.get(id=uid)
            chng.set_password(chngpass)
            chng.email = email
            chng.username = email
            chng.first_name = first
            chng.last_name = last
            chng.save()
        else:
            messages.error(request,"INCORRECT PASSWORD")
        base = reverse('userpage')
        userid = ({'uid':uid})
        return redirect('{}?{}'.format(base,userid))