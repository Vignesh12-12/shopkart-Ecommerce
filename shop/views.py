from django.shortcuts import render,redirect
from django.http import JsonResponse
from . models import *
from shop.form import Customuserform
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
import json

# Create your views here.
def home(request):
    products=Product.objects.filter(trending=1)
    return render(request,"shop/index.html",{"products":products})

def remove_fav(request,fid):
    favitem=Favourite.objects.get(id=fid)
    favitem.delete()
    return redirect('favviewpage')

def favviewpage(request):
    if request.user.is_authenticated:
        fav=Favourite.objects.filter(user=request.user)
        return render(request,'shop/fav.html',{'fav':fav})
    else:
        return redirect('home')

def fav_page(request):
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
           data=json.load(request)
           product_id=data['pid']
           product_status=Product.objects.get(id=product_id)
           if product_status:
               if Favourite.objects.filter(user=request.user.id,product_id=product_id):
                return JsonResponse({"status":"already added"}, status=200)
               else:
                Favourite.objects.create(user=request.user,product_id=product_id)
                return JsonResponse({'status':'Product Added to Favourite'}, status=200)     
        else:
           return JsonResponse({'status':'Login to add Favourite'}, status=200)      
    else:
        return JsonResponse({'status':'Invalid Access'}, status=200)

def remove_cart(request,cid):
    cartitem=Cart.objects.get(id=cid)
    cartitem.delete()
    return redirect('/cart')

def cart_page(request):
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user)
        return render(request,'shop/cart.html',{'cart':cart})
    else:
        return redirect('home')

def add_to_cart(request):
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
           data=json.load(request)
           product_qty=data['product_qty']
           product_id=data['pid']
           product_status=Product.objects.get(id=product_id)
           if product_status:
               if Cart.objects.filter(user=request.user.id,product_id=product_id):
                   return JsonResponse({'status':'Product Already in Cart'}, status=200) 
               else:
                   if product_status.quantity>=product_qty:
                       Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
                       return JsonResponse({'status':'Product Added to Cart'}, status=200)
                   else:
                       return JsonResponse({'status':'Product Stock Not Available'}, status=200)
                 
        else:
           return JsonResponse({'status':'Login to add cart'}, status=200)      
       
    else:
        return JsonResponse({'status':'Invalid Access'}, status=200)

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"logged out successfully")
        return redirect('home')


def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method=="POST":
            name=request.POST.get("username")
            pwd=request.POST.get("password")
            user=authenticate(request,username=name,password=pwd)
            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                messages.error(request,"Invalid username or password")
                return redirect("/login")

    return render(request,"shop/login.html")

def register(request):
    form=Customuserform()
    if request.method=="POST":
        form=Customuserform(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Account created successfully!! Login Now")
            return redirect('login')
    return render(request,"shop/register.html",{'form':form})

def collections(request):
    category=Category.objects.filter(status=0)
    return render(request,"shop/collections.html",{"category":category})

def collectionsview(request,name):
    if(Category.objects.filter(name=name,status=0)):
        products=Product.objects.filter(category__name=name)
        return render(request,"shop/products/index.html",{"products":products,"category_name":name})
    else:
        messages.warning(request,"no such file directory found")
        return redirect("collections")
    
def product_details(request, cname, pname):
    if (Category.objects.filter(name=cname, status=0)):
        if (Product.objects.filter(name=pname, status=0)):
            products=Product.objects.filter(name=pname, status=0).first()
            return render(request,"shop/products/product_details.html",{"products":products})
        else:
            messages.error(request, "No Such product Found")
            return redirect('collections')
    else:
        messages.error(request, "No Such Category Found")
        return redirect('collections')
    