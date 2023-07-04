from django.shortcuts import render,redirect
from .models import *
from django.http import HttpResponse
from accounts.models import User
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Max,Min,Count,Avg
import time

def wishlist(request):
    print("this is wishlist")
    wishlist=Wishlist.objects.filter(user=request.user)
    print("cark ok") 
    
    context={'wishlist':wishlist} 
    print("context ok")
    return render(request,'wishlist/wishlist.html',context)

def add_wishlist(request):
    if request.method=='POST':
        if request.user.is_authenticated:
            print('wishpostmethod')
            produ_id=request.POST.get('product_id')
            use=request.user.id
            print(use)
            print("wishproduct_id is",produ_id)
            product_check=Product.objects.get(uid=produ_id)
          
            if(product_check):
                print("wishid are equal")
                if(Wishlist.objects.filter(user=request.user.id,product_id=produ_id)):
                    print("entering cart")
                    
                    return JsonResponse({'status':"Product already in wishlist"})
                else:
                        print("i am in else")
                        product_quntity=int(request.POST.get('qty'))
                        print("the quantity is",product_quntity)
                        
                        pro_price=request.POST.get('price')
                        
                        print("productquantity is ok",pro_price)
                        Wishlist.objects.create(product_id= produ_id, user_id=request.user.id,product_qty=product_quntity, product_price=pro_price)
                        print("product added ")
                       
                        return JsonResponse({'status':"product added to the wishlist successfully"})
                        
            else:
                return JsonResponse({'status':"no such product found"})
        else:
             return JsonResponse({'status':"please login"})
            
    time.sleep(1)
    return redirect('/')

def delete_wishlist(request):
    if request.method=='POST':
        produ_id=request.POST.get('product_id')
        print(produ_id)
        if(Wishlist.objects.filter(user=request.user.id,product_id=produ_id)):
            print("deleted form")
            wishlistitem=Wishlist.objects.get(product_id=produ_id,user=request.user.id)
            wishlistitem.delete()
            return JsonResponse({'status':"product deleted successfully"})   
        return JsonResponse({'status':"No item in whishlist"})  
    time.sleep(1) 
    return redirect('/')


def wishlistempty(request):
    return render(request,'wishlist/wishlist_empty.html')