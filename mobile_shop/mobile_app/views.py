from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from .models import *
import os
import math,random

# Create your views here.


def shop_log(req):
    if 'mshop' in req.session:
        return redirect(shop_home)
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
        return render(req,'shop/shop_home.html',{'product':product,'details':details})
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
        product=req.POST['product']
        ecolor=req.POST['ed_color']
        estorage=req.POST['ed_storage']
        eram=req.POST['ed_ram']
        eprice=req.POST['ed_price']
        estock=req.POST['ed_stock']
        data=Details.objects.create(pro=Product.objects.get(pk=product),color=ecolor,storage=estorage,ram=eram,price=eprice,stock=estock)
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
        otp=OTP(req)
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
        return render(req,'user/user_home.html',{'products':products,'details':details})
    else:
        return redirect(shop_log)
def user_view(req,pid):
    data=Product.objects.get(pk=pid)
    data1=Details.objects.filter(pro=pid)
    data2=Details.objects.get(pro=pid,pk=data1[0].pk)
    ram=data2.ram
    if req.GET.get('ram'):
        ram=req.GET.get('ram')
        data2=Details.objects.get(pro=pid,pk=ram)
        if req.GET.get('storage'):
            storage=req.GET.get('storage')
            data2=Details.objects.get(pro=pid,pk=storage)
    return render(req,'user/user_view.html',{'data':data,'data1':data1,'data2':data2,'ram':ram})


#-------------------------------------------------------

def add_cart(req,cid):
        
    detail=Details.objects.get(pk=cid)
    user=User.objects.get(username=req.session['user'])
    try:
        cart=Cart.objects.get(details=detail,user=user)
        cart.qty+=1
        cart.save()
    except:
        data=Cart.objects.create(details=detail,user=user,qty=1)
        data.save()
    return redirect(view_cart)
    
def view_cart(req):
    user=User.objects.get(username=req.session['user'])
    data=Cart.objects.filter(user=user)
    return render(req,'user/cart.html',{'cart':data})

def qty_incr(req,cid):
    if 'user' in req.session:
        data=Cart.objects.get(pk=cid)
        stock=int(data.details.stock)
        if stock >0:
            data.qty+=1
            data.save()
        return redirect(view_cart)
    else:
        return redirect(shop_log)
def qty_decr(req,cid):
    data=Cart.objects.get(pk=cid)
    data.qty-=1
    data.save()
    if data.qty==0:
        data.delete()
    return redirect(view_cart)
def buy_now(req,pid):
    detail=Details.objects.get(pk=pid)
    user=User.objects.get(username=req.session['user'])
    qty=1
    price=detail.price
    buy=Buy.objects.create(product=detail,user=user,qty=qty,t_price=price)
    buy.save()
    return redirect(user_bookings)
def cart_buy(req,cid):
    cart=Cart.objects.get(pk=cid)
    cprice=int(cart.details.price)
    tprice=cart.qty*cprice
    buy=Buy.objects.create(product=cart.details,user=cart.user,qty=cart.qty,t_price=tprice)
    buy.save()
    return redirect(user_bookings)
def user_bookings(req):
    user=User.objects.get(username=req.session['user'])
    booking=Buy.objects.filter(user=user)[::-1]
    return render(req,'user/booking.html',{'booking':booking})