from django.shortcuts import render,redirect
from django.http import JsonResponse
from accounts.models import User
from products.models import *
from .models import *
from django.contrib import messages
from userprofile.models import *
from django.db.models import Q
from oders.models import *
from userprofile.models import *
import time

# Create your views here.
def add_cart(request):
    if request.method=='POST':
        if request.user.is_authenticated:
           
            produ_id=request.POST.get('product_id')
            use=request.user
         
            clr=request.POST.get('colorElement')
         
            color_name=ColorVariant.objects.get(uid=clr)
           
            siz=request.POST.get('sizeElement')
          
            sized=request.POST.get('size')
            product_check=Product.objects.get(uid=produ_id)
          
            productatt = ProductAttribute.objects.get(Q(product_id=produ_id) & Q(colorVariant_id=clr)& Q(sizevariant_id=siz))
           
            if(product_check):
                
                if(Cart.objects.filter(user=request.user,product_id= produ_id,productattr_id=productatt.uid)):
                  
                    return JsonResponse({'status':"Product already in cart"})
                else:
                    
                    productatt_quntity=int(request.POST.get('qty'))
                  
                    if productatt.quantity >=productatt_quntity:
                        pro_price=request.POST.get('price')
                        total= productatt_quntity*float(pro_price)
                        
                        
                        Cart.objects.create(product_id= produ_id, product_qty=productatt_quntity,user_id=request.user.id, product_price=pro_price,total_price=total,productattr_id=productatt.uid,color=color_name, size=sized)
                       
                        return JsonResponse({'status':"product added to the cart successfully"})
                    
                    else:
                        print("product cannot added")
                        return JsonResponse({'status':"Only"+str(productatt.quantity)+"quantity available"})  
            else:
                return JsonResponse({'status':"no such product found"})
        else:
             return JsonResponse({'status':"please login"})
            
    time.sleep(1)    
    return redirect('/')

def cart(request):
  
    out_of_stock = False 
    cart=Cart.objects.filter(user=request.user)
    wallet=Wallet.objects.filter(user=request.user)
    coupon = Cart.get_coupon(request.user)
   
    address=Address.objects.filter(user=request.user).order_by('created_at').last()
     
    available_coupon=Coupon.objects.all()
    grand_total = Cart.calculate_grand_total(request.user)
    for item in cart:
        if item.productattr.quantity < item.product_qty:
            out_of_stock = True 
            break
    context={'cart':cart,'grand_total':grand_total,'coupon':coupon,'address':address,'available_coupon':available_coupon,'out_of_stock': out_of_stock,'messages': messages.get_messages(request),'wallet':wallet} 
    
  
    return render(request,'cartify/cart.html',context)
def delete_cart(request):
    if request.method=='POST':
        produ_id=request.POST.get('product_id')
       
        if(Cart.objects.filter(user=request.user.id,productattr_id=produ_id)):
           
            cartitem=Cart.objects.get(productattr_id=produ_id,user=request.user.id)
            cartitem.delete()
            return JsonResponse({'status':"product deleted successfully"})   
        return JsonResponse({'status':"No item in cart"})   
    return redirect('/')

def update_cart(request):
    if request.method=='POST':
        produ_id=request.POST.get('product_id')
        print("update_productquantity is",produ_id)
        if(Cart.objects.filter(user=request.user.id,productattr_id=produ_id)):
         
            product_quntity=int(request.POST.get('qty'))
            pro_price=request.POST.get('price')
            pro_price = pro_price.replace('₹', '')
           
            total=product_quntity*float(pro_price)
            
           
            cart=Cart.objects.get(productattr_id=produ_id,user=request.user.id)
            cart.product_qty=product_quntity
            cart.total_price=total
            cart.save()
            return JsonResponse({'status':"quantity updated successfully"})
            
    return redirect('/')


def apply_coupon(request):
    print("entering coupon")
    user_carts = Cart.objects.filter(user=request.user)
    
    if user_carts.count() > 1:
        cart = user_carts.latest('created_at')
    elif user_carts.exists():
        cart = user_carts.first()
    else:
        return redirect('/cartify/cart')
    
    grand_total = Cart.calculate_grand_total(request.user)
    print("cart le coupon", cart.coupon)
    
    if request.method == 'POST':
        coupon = request.POST['coupon_code']
        print(coupon)
        
        try:
            coupon_obj = Coupon.objects.get(coupon_code__icontains=coupon) 
           
            
            if coupon_obj.is_expired:
                messages.warning(request, "This coupon is expired")
                return JsonResponse({'status': "This coupon is expired"})
            else:
                coupon_used = Order.objects.filter(user=request.user, coupon_id=coupon_obj.id)
                
                if cart.coupon:
                    print("coupon already exist")
                    messages.warning(request, "You have already used this coupon")
                    return JsonResponse({'status': "Coupon already exists"})
                
                else: 
                    if 'FIRST PURCHASE' in coupon_obj.coupon_code:
                        if coupon_used:
                           
                            messages.warning(request, "Coupon is only applicable for the first purchase!!")
                            return JsonResponse({'status': "Coupon is only applicable for the first purchase"})
                        
                        else:
                           
                           
                            cart.coupon = coupon_obj
                            cart.save()
                            messages.success(request, 'You are using' + ' ' + coupon + ' coupon')
                            return JsonResponse({'status': "Coupon Applied"})
                    else:
                        if grand_total >= coupon_obj.minimum_amount:
                            cart.coupon = coupon_obj
                            cart.save()
                            messages.success(request, 'You are using' + ' ' + coupon + ' coupon')
                            return JsonResponse({'status': "Coupon Applied"})
                        else:
                            messages.warning(request, "Coupon is not applicable for the current bag amount!!")
                            return JsonResponse({'status': "Coupon is not applicable for the current bag amount"})
               
        except Coupon.DoesNotExist:
            print("invalid")
            return JsonResponse({'status': "Invalid Coupon"})
        
    return redirect('/cartify/cart')

    
def checkout(request):
    address=Address.objects.filter(user=request.user)
    cart=Cart.objects.filter(user=request.user)
    grand_total = Cart.calculate_grand_total(request.user)
    wallet=Wallet.objects.filter(user=request.user).first()
  
    context={'address':address,'cart':cart,'grand_total': grand_total,'wallet':wallet}
    return render(request,'cartify/checkout.html',context)
def coupon(request):
    available_coupon=Coupon.objects.all()
   
    context={'available_coupon':available_coupon}
    return render(request,'cartify/coupon.html',context)

def cartempty(request):
    return render(request,'cartify/cartempty.html')
       
    
        
