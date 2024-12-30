from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from .models import *
import os

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
        categor=req.POST['cat']
        img=req.FILES['aimg']
        pro=Product.objects.create(pid=pid,pname=name,pdis=dis,img=img,cate=Category.objects.get(cname=categor))
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
        dt=Details.objects.create(color=color,storage=storage,ram=ram,price=price,stock=stock,pro=Product.objects.get(pname=products))
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
#----------USER------------
def user_reg(req):
    if req.method=='POST':
        uname=req.POST['username']
        email=req.POST['email']
        pswd=req.POST['password']
        try:
            data=User.objects.create_user(first_name=uname,email=email,username=email,password=pswd)
            data.save()
            
            return redirect(shop_log)
        except:
            messages.warning(req,'Email Already Exit')
            return redirect(user_reg)
    else:
        return render(req,'user/register.html')
def user_home(req):
    return render(req,'user/user_home.html')