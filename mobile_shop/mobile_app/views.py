from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from .models import *
import os
import math,random
from django.http import JsonResponse,HttpResponse
import razorpay
import json
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def front(req):
    products=Product.objects.all()
    details=Details.objects.all()
    data=Category.objects.all()
    return render(req,'front.html',{'products':products,'details':details,'data':data})


def home(req):
    if 'user' in req.session:
        return redirect(user_home)
    if 'mshop' in req.session:
        return redirect(shop_home)

    products=Product.objects.all()
    details=Details.objects.all()
    data=Category.objects.all()
    return render(req,'home.html',{'products':products,'details':details,'data':data})
def shop_log(req):
    if 'mshop' in req.session:
        return redirect(shop_home)
    if 'user' in req.session:
        return redirect(user_home)
    if req.method=='POST':
        uname=req.POST['username']
        password=req.POST['password']
        mshop=authenticate(username=uname,password=password)
        if mshop:
            login(req,mshop)
            if mshop.is_superuser:
                req.session['mshop']=uname
                return redirect(shop_home)
            else:
                req.session['user']=uname
                return redirect(user_home)
        else:
            messages.warning(req,'Invalid user name or password')
            return redirect(shop_log)
    else:
       return render(req,'shop_login.html')


def shop_logout(req):
    logout(req)
    req.session.flush()
    return redirect(shop_log)



#-----------OWNER-------------
def shop_home(req):
    if 'mshop' in req.session:
        product=Product.objects.all()
        details=Details.objects.all()
        data=Category.objects.all()
        return render(req,'shop/shop_home.html',{'product':product,'details':details,'data':data})
    else:
        return redirect(shop_log)

def add_pro(req):
    if req.method=='POST':
        pid=req.POST['aid']
        name=req.POST['aname']
        dis=req.POST['adis']
        categorie=req.POST['cat']
        img=req.FILES['aimg']
        pro=Product.objects.create(pid=pid,pname=name,pdis=dis,img=img,cate=Category.objects.get(cname=categorie))
        pro.save()
        return redirect(details)
    else:
        data=Category.objects.all()
        return render(req,'shop/add_pro.html',{'data':data})

def admin_view(req,pid):
    if 'mshop' in req.session:
        pro=Product.objects.filter(pk=pid)
        detail=Details.objects.filter(pro=pid)
        category=Category.objects.all()
        return render(req,'shop/view.html',{'pro':pro,'details':detail,'cat':category})
    else:
        return redirect(shop_log)
def category(req):
    if req.method=='POST':
        name=req.POST['bname']
        categ=Category.objects.create(cname=name)
        categ.save()
        return redirect(shop_home)
    else:
        data=Category.objects.all()
        return render(req,'shop/category.html',{'data':data})

def details(req):
    if req.method=='POST':
        color=req.POST['color']
        storage=req.POST['storage']
        ram=req.POST['ram']
        price=req.POST['price']
        stock=req.POST['stock']
        products=req.POST['p_id']
        dt=Details.objects.create(color=color,storage=storage,ram=ram,price=price,stock=stock,pro=Product.objects.get(pk=products))
        dt.save()
        return redirect(shop_home)
    else:
        data=Product.objects.all()
        return render(req,'shop/details.html',{'data1':data})

def delete(req,pid):
    data=Product.objects.get(pk=pid)
    file=data.img.url
    file=file.split('/')[-1]
    os.remove('media/'+file)
    data.delete()
    return redirect(shop_home)
def edit_pro(req,pid):
    if 'mshop' in req.session:
        if req.method=='POST':
            epid=req.POST['e_pid']
            ename=req.POST['e_pname']
            edis=req.POST['e_pdis']
            img=req.FILES.get('e_img')
            if img:
                Product.objects.filter(pk=pid).update(pid=epid,pname=ename,pdis=edis)
                data=Product.objects.get(pk=id)
                # url=data.img.url
                # og_path=url.split('/')[-1]
                # os.remove('media/'+og_path)
                data.img=img
                data.save()
            else:
                Product.objects.filter(pk=pid).update(pname=ename,pdis=edis)
            return redirect(shop_home)

        else:
            data=Product.objects.get(pk=pid)
            return render(req,'shop/edit_pro.html',{'epro':data})
    else:
        return redirect(shop_log)

def edit_details(req,pid):
    if req.method=='POST':
        eimg=req.POST['ed_img']
        product=req.POST['product']
        ecolor=req.POST['ed_color']
        estorage=req.POST['ed_storage']
        eram=req.POST['ed_ram']
        eprice=req.POST['ed_price']
        estock=req.POST['ed_stock']
        data=Details.objects.create(pro=Product.objects.get(pk=product),img=eimg,color=ecolor,storage=estorage,ram=eram,price=eprice,stock=estock)
        data.save()
        return redirect("edit_details",pid=pid)
    else:
        data=Details.objects.filter(pro=pid)
        data1=Product.objects.get(pk=pid)
        return render(req,'shop/edit_details.html',{'data':data,'data1':data1})
def delete_details(req,pid):
    data=Details.objects.get(pk=pid)
    data.delete()
    return redirect(shop_home)

def ad_booking(req):
    data=Buy.objects.all()[::-1]
    return render(req,'shop/bookings.html',{'booking':data})

#----------USER------------

def OTP(req):
    digits= "0123456789"
    OTP= ""
    for i in range(6):
        OTP += digits[math.floor(random.random()*10)]
    return OTP
def user_reg(req):
    if req.method=='POST':
        uname=req.POST['username']
        email=req.POST['email']
        pswd=req.POST['password']
        confirm_password = req.POST['confirm_password']
        otp=OTP(req)
        if pswd != confirm_password:
            messages.error(req, "Passwords do not match!")
            return redirect(user_reg)
        if User.objects.filter(email=email).exists():
            messages.error(req,"Email is already Exits")
            return redirect(user_reg)
        else:
            send_mail('Your OTP for Registaion',f"OTP for Registration {otp}",settings.EMAIL_HOST_USER,[email])
            messages.success(req,"Registration Successfull.Check OTP")
            return redirect("validate",name=uname,password=pswd,email=email,otp=otp)

    else:
        return render(req,'user/register.html')

def validate(req,name,password,email,otp):
    if req.method=='POST':
        Otp=req.POST['Otp']
        if Otp==otp:
            data=User.objects.create_user(first_name=name,email=email,password=password,username=email)
            data.save()
            messages.success(req,"OTP verified Successfully")
            return redirect(shop_log)
        else:
            messages.error(req,"invalid Otp")
            return redirect("validate",name=name,password=password,email=email,otp=otp)
    else:
        return render(req,'user/validate.html',{'name':name,"pass":password,'emai':email,'otp':otp})



def user_home(req):
    if 'user' in req.session:
        products=Product.objects.all()
        details=Details.objects.all()
        data=Category.objects.all()
        return render(req,'user/user_home.html',{'products':products,'details':details,'data':data})
    else:
        return redirect(shop_log)


def brand_products(req, brand_id):
    brand = get_object_or_404(Category, pk=brand_id)
    products = Product.objects.filter(cate=brand)
    return render(req, 'user/brand_products.html', {'brand': brand, 'products': products})


#----------------------------------------------------

# def user_view(req,pid):
#     data=Product.objects.get(pk=pid)
#     data1=Details.objects.filter(pro=pid)
#     data2=Details.objects.get(pro=pid,pk=data1[0].pk)
#     ram=data2.ram
#     if req.GET.get('ram'):
#         ram=req.GET.get('ram')
#         data2=Details.objects.get(pro=pid,pk=ram)
#         if req.GET.get('storage'):
#             storage=req.GET.get('storage')
#             data2=Details.objects.get(pro=pid,pk=storage)
#     return render(req,'user/user_view.html',{'data':data,'data1':data1,'data2':data2,'ram':ram})

# def user_view(req, pid):
#     data = Product.objects.get(pk=pid)
#     data1 = Details.objects.filter(pro=pid)
#     ram_options = data1.values_list('ram', flat=True).distinct()
#     storage_options = data1.values_list('storage', flat=True).distinct()
#     data2 = data1[0] if data1.exists() else None
#     ram = req.GET.get('ram')
#     if ram:
#         data2 = data1.filter(ram=ram).first()

#     storage = req.GET.get('storage')

#     if storage and data2:
#         data2 = data1.filter(ram=data2.ram, storage=storage).first()

#     return render(req, 'user/user_view1.html', {
#         'data': data,
#         'data1': data1,
#         'data2': data2,
#         'ram_options':ram_options,
#         'storage_options':storage_options,
#         'ram': ram,
#         'storage': storage,
#     })

# def user_view(req, pid):
#     data = Product.objects.get(pk=pid)
#     data1 = Details.objects.filter(pro=pid)
#     data3=Category.objects.all()
#     data4=Details.objects.get(pro=pid,pk=data1[0].pk)
#     ram_options = data1.values_list('ram', flat=True).distinct()
#     storage_options = data1.values_list('storage', flat=True).distinct()
#     data2 = data1[0] if data1.exists() else None
#     img=req.GET.get('img')
#     color=req.GET.get('color')
#     ram = req.GET.get('ram')
#     storage = req.GET.get('storage')
#     # Filter based on the selected RAM and storage
#     if ram:
#         data2 = data1.filter(ram=ram).first()

#     if storage and data2:
#         data2 = data1.filter(ram=data2.ram, storage=storage).first()
#     # Check if the selected combination is valid
#     valid_combination = data2 is not None
#     if req.GET.get('color'):
#         color=req.GET.get('color')

#     return render(req, 'user/user_view1.html', {
#         'data': data,
#         'data1': data1,
#         'data2': data2,
#         'data3':data3,
#         'data4':data4,

#         'ram_options': ram_options,
#         'storage_options': storage_options,
#         'ram': ram,
#         'storage': storage,
#         'valid_combination': valid_combination,
#     })


def user_view(req, pid):
    if 'user' in req.session:
        data = Product.objects.get(pk=pid)
        data1 = Details.objects.filter(pro=pid)
        data3 = Category.objects.all()


        # Fetch details for the first product in data1 (this could be optimized based on your model design)
        data4 = data1.first()  # Use the first matching record
        

        # Get unique RAM and storage options
        ram_options = data1.values_list('ram', flat=True).distinct()
        storage_options = data1.values_list('storage', flat=True).distinct()
        color_options=data1.values_list('color', flat=True).distinct
        image_option=data1.values_list('img',flat=True).distinct()
        # Get selected parameters (color, ram, storage) from GET
        color = req.GET.get('color', '')  # Default to empty string if not set
        ram = req.GET.get('ram', '')
        storage = req.GET.get('storage', '')
        img=req.GET.get('img','')
        # Filter based on the selected RAM, storage, and color
        if ram:
            data2 = data1.filter(ram=ram).first()  # Find the first matching RAM
        else:
            data2 = data1.first()  # Default to first option if RAM isn't selected
        
        if storage and data2:
            data2 = data1.filter(ram=data2.ram, storage=storage).first()  # Filter by storage as well
        if color and data2:
            data2 = data1.filter(ram=data2.ram, storage=data2.storage, color=color).first()  # Filter by color
        stock=int(data4.stock)
        # Check if the combination is valid
        valid_combination = data2 is not None and stock > 0
        # Pass all data to the template
        return render(req, 'user/user_view1.html', {
            'data': data,
            'data1': data1,
            'data2': data2,
            'data3': data3,
            'data4': data4,
            'ram_options': ram_options,
            'storage_options': storage_options,
            'color_options': color_options,
            'ram': ram,
            'storage': storage,
            'color': color,
            'stock':stock,
            'valid_combination': valid_combination,  # This will control if the combination is valid
        })
    else:
        return redirect(shop_log)

#-------------------------------------------------------

def add_address(req):
    if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        data=Address.objects.filter(user=user)
        data2=Category.objects.all()
        if req.method=='POST':
            user=User.objects.get(username=req.session['user'])
            name=req.POST['name']
            phn=req.POST['phn']
            house=req.POST['house']
            street=req.POST['street']
            pin=req.POST['pin']
            state=req.POST['state']
            data=Address.objects.create(user=user,name=name,phn=phn,house=house,street=street,pin=pin,state=state)
            data.save()
            return redirect(add_address)
        else:

            return render(req,'user/address.html',{'data':data,'data2':data2})
    else:
        return redirect(shop_log)

def delete_address(req, pid):
    if 'user' in req.session:
        data=Address.objects.get(pk=pid)
        data.delete()
        return redirect(add_address)
    else:
        return redirect(shop_log)

def add_cart(req,cid):
    if 'user' in req.session:
        detail=Details.objects.get(pk=cid)
        user=User.objects.get(username=req.session['user'])
        try:
            cart=Cart.objects.get(details=detail,user=user)
            cart.qty+=1
            cart.save()
        except:
            data=Cart.objects.create(details=detail,user=user,qty=1)
            data.save()
        stock=int(detail.stock)
        stock-=1
        detail.save()
        return redirect(view_cart)
    else:
        return redirect(shop_log)

def view_cart(req):
    if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        data=Cart.objects.filter(user=user)
        data2=Category.objects.all()
        total = sum(float(item.details.price) * item.qty for item in data)
        return render(req,'user/cart.html',{'cart':data,'data2':data2})
    else:
        return redirect(shop_log)
def deleteCart(req,pid):
    if 'user' in req.session:
        data=Cart.objects.get(pk=pid)
        data.delete()
        return redirect(view_cart)
    else:
        return redirect(shop_log)

def qty_incr(req,cid):
    if 'user' in req.session:
        data=Cart.objects.get(pk=cid)
        stock=int(data.details.stock)
        
        if stock >0:
            data.qty+=1
            data.save()

            stock -= 1
            data.details.stock = stock  # Decrease stock of the product in inventory
            data.details.save()
        else:
                # If no stock is available, show out of stock message
                messages.error(req, "Sorry, this item is out of stock.")
        
        return redirect(view_cart)

    else:
        return redirect(shop_log)
def qty_decr(req,cid):
    if 'user' in req.session:
        data=Cart.objects.get(pk=cid)
        data.qty-=1
        data.save()
        if data.qty==0:
            data.delete()
        return redirect(view_cart)

    else:
        return redirect(shop_log)

def buy_now(req,pid):
    if 'user' in req.session:
        detail=Details.objects.get(pk=pid)
        user=User.objects.get(username=req.session['user'])
        qty=1
        price=detail.price
        data=Address.objects.filter(user=user)
        stock=int(detail.stock)
        stock-=1
        detail.stock=str(stock)
        detail.save()
        if data:
            return redirect('place_order',detail=detail.pk,data=data.first().pk,qty=qty,price=price)
        else:
            if req.method=='POST':
                user=User.objects.get(username=req.session['user'])
                name=req.POST['name']
                phn=req.POST['phn']
                house=req.POST['house']
                street=req.POST['street']
                pin=req.POST['pin']
                state=req.POST['state']
                data=Address.objects.create(user=user,name=name,phn=phn,house=house,street=street,pin=pin,state=state)
                data.save()
                return redirect("place_order",detail=detail.pk,data=data.pk,qty=qty,price=price)
            else:
                return render(req,'user/address.html')
    else:
        return redirect(shop_log)

def place_order(req,detail,data,qty,price):
    if 'user' in req.session:
        detail=Details.objects.get(pk=detail)
        user=User.objects.get(username=req.session['user'])
        data=Address.objects.filter(user=user)
        req.session['pid']=detail.pk
        if req.method=='POST':
            address=req.POST['address']
            pay=req.POST['pay']
            addr=Address.objects.get(user=user,pk=address)
        else:
            return render(req,'user/order.html',{'details':detail,'data':data,'price':price})
        req.session['address']=addr.pk

        if pay == 'paynow' :
           return redirect("order_payment",pid=detail.pk)
        else:
            return redirect(bookings)

    else:
        return redirect(shop_log)

def order_payment(req,pid):
    if 'user' in req.session:
        user = User.objects.get(username=req.session['user'])
        address=Address.objects.get(pk=req.session['address'])
        name = user.first_name
        data=Details.objects.get(pk=pid)
        amount = data.price
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        razorpay_order = client.order.create(
            {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
        )
        order_id=razorpay_order['id']
        order = Order.objects.create(
            name=name, amount=amount, provider_order_id=order_id
        )
        order.save()
        return render(
            req,
            "user/payment.html",
            {
                "callback_url": "http://127.0.0.1:8000/callback",
                "razorpay_key": settings.RAZORPAY_KEY_ID,
                "order": order,
            },
        )
    else:
        return render(shop_log)

@csrf_exempt
def callback(request):

    def verify_signature(response_data):
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        return client.utility.verify_payment_signature(response_data)

    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.signature_id = signature_id
        order.save()
        if not verify_signature(request.POST):
            order.status = PaymentStatus.SUCCESS
            order.save()
            return render(request, "callback.html", context={"status": order.status})

        else:
            order.status = PaymentStatus.FAILURE
            order.save()
            # return render(request, "callback.html", context={"status": order.status})
            return redirect(bookings)



    else:
        payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
        provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
            "order_id"
        )
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.status = PaymentStatus.FAILURE
        order.save()
        return render(request, "callback.html", context={"status": order.status})

def bookings(req):
    if 'user' in req.session:
        address=Address.objects.get(pk=req.session['address'])
        detail=Details.objects.get(pk=req.session['pid'])
        user=User.objects.get(username=req.session['user'])
        data=Buy.objects.create(user=user,product=detail,qty=1,t_price=detail.price,address=Address.objects.get(pk=address.pk))
        data.save()
        stock=int(detail.stock)
        stock-=1
        detail.save()
        return redirect(user_bookings)
    else:
        return redirect(shop_log)

def cart_buy(req):
    if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        cart=Cart.objects.filter(user=user)
        
        total=0
        for i in cart:
            qty=i.qty
            cprice=int(i.details.price)
            tprice=qty*cprice
            total+=tprice
        data=Address.objects.filter(user=user)
        
        if data:
            return redirect('place_order2',qty=qty,tprice=tprice,total=total)
        else:
            if req.method=='POST':
                user=User.objects.get(username=req.session['user'])
                name=req.POST['name']
                phn=req.POST['phn']
                house=req.POST['house']
                street=req.POST['street']
                pin=req.POST['pin']
                state=req.POST['state']
                data=Address.objects.create(user=user,name=name,phn=phn,house=house,street=street,pin=pin,state=state)
                data.save()
                return redirect('place_order2',qty=qty,tprice=tprice,total=total)
            else:
                return render(req,'user/address.html')
    else:
        return redirect(shop_log)





def place_order2(req,qty,tprice,total):
    if 'user' in req.session:
       
        user=User.objects.get(username=req.session['user'])
        data=Address.objects.filter(user=user)
        cart=Cart.objects.filter(user=user)
        if req.method=='POST':
            address=req.POST['address']
            pay=req.POST['pay']
            addr=Address.objects.get(user=user,pk=address)
        else:
            return render(req,'user/order2.html',{'cart':cart,'data':data,'qty':qty,'tprice':tprice,'total':total})
        req.session['address']=addr.pk


        if pay == 'paynow' :
           return redirect("order_payment2")
        else:
            return redirect(bookings2)
        
    else:
        return redirect(shop_log)

# def payment(req,pid,address):
#     if 'user' in req.session:
#         data=Details.objects.get(pk=pid)
#         price=data.price
#         addr=Address.objects.get(pk=address)
#         return render(req,'user/payment.html',{'price':price,'data':data,'address':addr})
#     else:
#         return redirect(shop_log)



def order_payment2(req):
    if 'user' in req.session:
        user = User.objects.get(username=req.session['user'])
        name = user.first_name
        # data=Details.objects.get(pk=address)
        cart=Cart.objects.filter(user=user)
        amount=0
        for i in cart:
            amount +=float(i.details.price)*i.qty
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        razorpay_order = client.order.create(
            {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
        )
        order_id=razorpay_order['id']
        order = Order.objects.create(
            name=name, amount=amount, provider_order_id=order_id
        )
        order.save()
        return render(
            req,
            "user/payment.html",
            {
                "callback_url": "http://127.0.0.1:8000/callback2",
                "razorpay_key": settings.RAZORPAY_KEY_ID,
                "order": order,
            },
        )
    else:
        return render(shop_log)

@csrf_exempt
def callback2(request):
    def verify_signature(response_data):
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        return client.utility.verify_payment_signature(response_data)

    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.signature_id = signature_id
        order.save()
        if not verify_signature(request.POST):
            order.status = PaymentStatus.SUCCESS
            order.save()
            # return render(request, "callback.html", context={"status": order.status})
            return redirect(bookings2)

        else:
            order.status = PaymentStatus.FAILURE
            order.save()
            # return render(request, "callback.html", context={"status": order.status})
            return redirect(bookings2)



    else:
        payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
        provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
            "order_id"
        )
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.status = PaymentStatus.FAILURE
        order.save()
        return render(request, "callback.html", context={"status": order.status})

def bookings2(req):
    if 'user' in req.session:
        address=Address.objects.get(pk=req.session['address'])
        user=User.objects.get(username=req.session['user'])
        cart=Cart.objects.filter(user=user)

        for i in cart:
            price=float(i.details.price)*i.qty
            data=Buy.objects.create(user=i.user,product=i.details,t_price=price,qty=i.qty,address=Address.objects.get(pk=address.pk))
            data.save()
        cart.delete()
        return redirect(user_bookings)
    else:
        return redirect(shop_log)


def user_bookings(req):
    if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        booking=Buy.objects.filter(user=user)[::-1]
        data=Category.objects.all()
        return render(req,'user/user_booking.html',{'booking':booking,'data':data})
    else:
        return redirect(shop_log)
def delete_bookings(req,pid):
    if 'user' in req.session:
        data=Buy.objects.get(pk=pid)
        data.delete()
        return redirect(user_bookings)
    else:
        return redirect(shop_log)