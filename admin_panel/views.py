from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.cache import never_cache
from django.contrib import messages
from accounts.models import User
from products.models import *
from .forms import *
from cartify.models import *
from oders.models import *
from django.db.models import Max,Min,Count,Avg
from django.db.models.functions import ExtractMonth,ExtractWeek,ExtractYear,Cast
from django.shortcuts import get_object_or_404
from .models import *
from django.core.paginator import Paginator
from datetime import datetime
from django.db.models import Q
from django.core.mail import send_mail
import uuid
from django.db.models import Max,Min,Count,Sum
from django.utils import timezone
import calendar
import json
from collections import defaultdict
from django.db.models import F
from django.db.models import CharField

@never_cache
def adminlogin(request):
    print('how') 
    list=Order.objects.all()
    new=orderitem.objects.all().order_by('-id')[:5]
    top_selling_products = orderitem.objects.filter(status='Successfully Delivered').values('product_id').annotate(total_quantity=Sum('product_qty')).order_by('-total_quantity')[:10]
    top_selling_products_data = []

    for item in top_selling_products:
        product_id = item['product_id']
        total_quantity = item['total_quantity']

      
        product = Product.objects.get(uid=product_id)
        product_name = product.product_name

        top_selling_products_data.append({
            'product': product_name,
            'total_quantity': total_quantity
        })


    graph = orderitem.objects.filter(
        Q(status='Pending') | Q(status='Successfully Delivered') | Q(status='Cancelled') | Q(status='return')
    ).annotate(
        month=ExtractMonth('order__created_at'),
        category=Cast('product__category', output_field=CharField())  # Convert UUID to string
    ).values('month', 'status', 'category').annotate(count=Count('id')).values('month', 'status', 'category', 'count')

    delmonthNumber = []
    deltotalOrders = []
    returntotalOrders = []
    canceltotalOrders = []
    pendingtotalOrders = []
    default_value = 0
    total_order_count = defaultdict(int)
    category_orders = defaultdict(int)
    monthNumbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]  
    monthNames = [calendar.month_name[monthNumber] for monthNumber in monthNumbers]

    for g in graph:
        month = g['month']
        status = g['status']
        category = g['category']
        count = g['count']

        if status == 'Successfully Delivered':
            delmonthNumber.append(monthNames[month - 1])
            deltotalOrders.append(count)
        elif status == 'return':
            delmonthNumber.append(monthNames[month - 1])
            returntotalOrders.append(count)
        elif status == 'Cancelled':
            delmonthNumber.append(monthNames[month - 1])
            canceltotalOrders.append(count)
        elif status == 'Pending':
            delmonthNumber.append(monthNames[month - 1])
            pendingtotalOrders.append(count)

        total_order_count[monthNames[month - 1]] += count
        category_orders[category] += count

    # Retrieve category-wise order count data
    category_order_counts = dict(category_orders)
    category_order_counts = {str(key): value for key, value in category_order_counts.items()}

    context={ 'delmonthNumber': delmonthNumber,
        'deltotalOrders': deltotalOrders,
        'returntotalOrders': returntotalOrders,
        'canceltotalOrders': canceltotalOrders,
        'pendingtotalOrders': pendingtotalOrders,
        'total_order_count': json.dumps(total_order_count), 'category_order_counts': json.dumps(category_order_counts),'default_value':default_value ,'list':list,'new':new,'top_selling_products': top_selling_products_data}
    if request.user.is_authenticated:
        if request.user.is_superuser:
           
            return render(request,'admin_panel/index.html',context)
    if request.method == 'POST':
      
        email=request.POST.get('email')
       
        password=request.POST.get('password')
        user=authenticate(request,email=email,password=password)
        if user is not None:
            if user.is_superuser:
                login(request,user)
                
                return render(request,'admin_panel/index.html',context)
            else:
                return redirect('adminlogin')
        else:
            return redirect('adminlogin')

    return render(request,'admin_panel/login.html')
@never_cache  
def adminlogout(request):
    if User is not None:
        logout(request)
    return redirect('adminlogin')

def addproducts(request):
    return render(request,'admin_panel/add-product.html')
@never_cache 
def mainpage(request):
    
    list=Order.objects.all()
    context={'list':list}
    return render(request,'admin_panel/index.html',context)
@never_cache 
def userdetails(request): 
    if request.user.is_authenticated:
        users=User.objects.exclude(is_superuser=True)
        paginator = Paginator(users, 1) 
        page = request.GET.get('page')
        users = paginator.get_page(page)
        
        details={'users':users}
        return render(request,'admin_panel/userdetails.html',details)
    else:
        return redirect('/admin_panel/adminlogin')


@never_cache
def adduser(request):
    if request.method == 'POST':
        print('hai')
        first_name=request.POST.get('first')
        mobile=request.POST.get('mobile')
        email=request.POST.get('email')
        password=request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')
        if password!=confirm_password:
            return HttpResponse("Passwords are not same!!!")
        if User.objects.filter(first_name=first_name).exists():
            return HttpResponse("username already taken")
        else:
            new_user=User.objects.create_user(email,mobile)
            new_user.first_name=first_name
            new_user.email=email
            new_user.mobile=mobile
            new_user.save()
            return redirect(userdetails)
    return render(request,'admin_panel/userdetails.html')

@never_cache 
def edit(request):
  
    if request.user.is_authenticated:
        user=User.objects.get()
        details={'user':user}
    return render(request,'update.html',details)
@never_cache 
def update(request,id):
    if request.method == 'POST':
       
        u_first_name=request.POST.get('first')
        
        u_mobile=request.POST.get('mobile')
        u_email=request.POST.get('email')
        u_is_blocked=request.POST.get('status')
        if u_is_blocked == 'active':
            u_blocked = False
        else:
            u_blocked = True
        

        user=User.objects.get(id=id)
        
        user.first_name=u_first_name
        user.mobile=u_mobile
        user.email=u_email
        user.is_blocked= u_blocked
        user.save()
        return redirect('/admin_panel/')
@never_cache 
def delete(request,id):
    
    user=User.objects.get(id=id)
    user.delete()
    details={'user':user}
    return redirect('/admin_panel/userdetails')
"""
def block(request,id):
    print('hai')
    user=User.objects.get(id=id)
    if  user.is_blocked==False:
         user.is_blocked=True
         user.save()
         print('hai')
         details={'action':'B'}
         return render(request,'admin_panel/userdetails.html',details)
    else:
         user.is_blocked=False
         user.save()
         details={'action':'N'}
         return render(request,'admin_panel/userdetails.html',details)
"""
@never_cache 
def product_details(request):
    products=Product.objects.all().order_by('-created_at')
    paginator = Paginator(products, 2) 
    page = request.GET.get('page')
    products = paginator.get_page(page)
    details={'products':products}
    return render(request,'admin_panel/products_manage.html',details)
@never_cache 
def product_delete(request,uid):
  
    user=Product.objects.get(uid=uid)
    user.delete()
    products=Product.objects.all()
    details={'products':products}
    return render(request,'admin_panel/products_manage.html',details)
@never_cache 
def product_update(request,uid):
    products=Product.objects.get(uid=uid)
    productvar=ProductAttribute.objects.filter(product_id=uid)
    
    if request.method == 'POST':
        product_form = ProductUpdateForm(request.POST, instance=products)
       
        variant_form = ProductVariantFormSet(request.POST, request.FILES,instance=product_form.instance)
       
        if product_form.is_valid() :
            product_form.save()
          
            variant_form.save()
            return redirect('/admin_panel/product_details')
        else:
         
            return HttpResponse('Form data is not valid. Please check the submitted data.')
    else:
        product_form = ProductUpdateForm(instance=products)
        variant_form = ProductVariantFormSet(instance=products)
       
        
        context={
            'form':product_form,
            'variant_form':variant_form, 
           
            }
    
    return render(request,'admin_panel/product_update.html',context)
@never_cache 
def adding_product(request):
   
    ProductVariantFormSet = inlineformset_factory(
        Product, ProductAttribute, form=ProductVariantForm, extra=3, can_delete=True
    )
    ProductImageFormSet = inlineformset_factory(
       ProductAttribute, ProductImage, form=ProductImageForm, extra=3, can_delete=True
    
    )
    if request.method == 'POST':
        product_form = ProductUpdateForm(request.POST)
        variant_form=ProductVariantFormSet(request.POST,request.FILES,instance=product_form.instance)
       
       
      
        if product_form.is_valid() and variant_form.is_valid() :
            
            product_form.save()  
            variant_form.save()
         
           
           
            return redirect('/admin_panel/product_details')
        else:
           
            return HttpResponse('Form data is not valid. Please check the submitted data.')
    else:
        product_form = ProductUpdateForm()
        
        variant_form = ProductVariantFormSet(instance=product_form.instance)
   
      
        context={
            'form':product_form ,
            'variant_form':variant_form, 
           
            
            }
        return render(request,'admin_panel/adding_product.html',context)
@never_cache 
def product_variations(request, uid):
    ProductImageFormSet = inlineformset_factory(
       ProductAttribute, ProductImage, form=ProductImageForm, extra=3, can_delete=True
    
    )
    variation =   ProductAttribute.objects.filter(product_id=uid)
    paginator = Paginator(variation, 2) 
    page = request.GET.get('page')
  
    variation = paginator.get_page(page)
 
    context={'variation':variation}
    return render(request,'admin_panel/variations.html',context)
@never_cache 
def add_image(request, uid):
    product_attribute = ProductAttribute.objects.get(uid=uid)
    
    ProductImageFormSet = inlineformset_factory(
        ProductAttribute, ProductImage, form=ProductImageForm, extra=3, can_delete=True
    )
    
    if request.method == 'POST':
        image_form = ProductImageFormSet(request.POST, request.FILES, instance=product_attribute)
        if image_form.is_valid():
          
            product_attribute.save()
            
           
            image_form.save()
            
            return redirect('/admin_panel/product_details')
    else:
        image_form = ProductImageFormSet(instance=product_attribute)
    
    context = {
        'image_form': image_form
    }
    return render(request, 'admin_panel/variation_image.html', context)
@never_cache 
def Category_details(request):
    if request.user.is_authenticated and  request.user.is_superuser:
        categories=Category.objects.all()
        context={'categories':categories}
        return render(request,'admin_panel/categories.html',context)
    else:
        return redirect('/admin_panel/mainpage')
@never_cache     
def category_delete(request,uid):
   
    user=Category.objects.get(uid=uid)
    user.delete()
    return redirect('/admin_panel/Category_details')
    

def add_category(request):
    if request.method == 'POST':
        form = CategoryUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            category_name = form.cleaned_data['category_name'].lower()
            offer = float(form.cleaned_data['offer'])

            if not Category.objects.filter(category_name__iexact=category_name).exists():
                if offer >= 0:
                    offer_with_percentage = offer
                    form.instance.offer = offer_with_percentage
                    form.save()
                    return redirect('/admin_panel/Category_details')
                else:
                    form.add_error('offer', 'Offer must be a positive number.')
            else:
                form.add_error('category_name', 'Category already exists.')
        else:
            print('Form not valid:', form.errors)
    else:
        form = CategoryUpdateForm()
    context = {
        'form': form,
        'image_form': form
    }
    return render(request, 'admin_panel/addcat.html', context)


@never_cache 
def category_update(request, uid):
    categories = Category.objects.get(uid=uid)
     

    if request.method == 'POST':
        form = CategoryUpdateForm(request.POST, instance=categories)

        if form.is_valid():
            offer = float(form.cleaned_data['offer'])
            if offer >= 0:
                form.save()
                return redirect('/admin_panel/Category_details')
            else:
                print("updation not working")
                form.cleaned_data['offer'] = None 
                form.add_error('offer', 'Offer must be a positive number.')
                
        else:
            print('Form not valid:', form.errors)
    else:
        form = CategoryUpdateForm(instance=categories)
    context = {
            'form': form,
            'image_form': form
        }

    return render(request, 'admin_panel/update_category.html', context)


@never_cache 
def add_coupon(request):
    coupon=Coupon.objects.all()
    context={'coupon':coupon}
    return render(request,'admin_panel/coupon.html',context)
@never_cache 
def delete_coupon(request,id):
   
    user=Coupon.objects.get(id=id)
    user.delete()
    return redirect('/admin_panel/add_coupon')
@never_cache 
def edit_coupon(request, id):
    coupon = Coupon.objects.get(id=id)
    if request.method == 'POST':
        form = CouponUpdateForm(request.POST, instance=coupon)
        if form.is_valid():
            discount_price = form.cleaned_data['discount_price']
            if discount_price <= 0:
                form.add_error('discount_price', 'Discount price must be a positive number.')
            else:
                form.save()
                return redirect('/admin_panel/view_coupon/{id}')  # Replace {id} with the actual coupon ID
    else:
        form = CouponUpdateForm(instance=coupon)
        context = {
            'form': form,
        }
    return render(request, 'admin_panel/editcoupon.html', context)

@never_cache 
def new_coupon(request):
    if request.method == 'POST':
        form = CouponUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            discount_price = form.cleaned_data['discount_price']
            if discount_price <= 0:
                form.add_error('discount_price', 'Discount price must be a positive number.')
            else:
                coupon_code = form.cleaned_data['coupon_code']
                if Coupon.objects.filter(coupon_code__iexact=coupon_code).exists():
                    form.add_error('coupon_code', 'Coupon with this code already exists.')
                else:
                    form.save()
                    return redirect('/admin_panel/add_coupon')
        else:
            print('Form not valid')
    else:
        form = CouponUpdateForm()

    context = {
        'form': form,
    }
    return render(request, 'admin_panel/addcoupon.html', context)



import calendar
def monthgraphical(request):
    list=Order.objects.all()
    new=orderitem.objects.all().order_by('-id')[:5]
    top_selling_products = orderitem.objects.filter(status='Successfully Delivered').values('product_id').annotate(total_quantity=Sum('product_qty')).order_by('-total_quantity')[:10]
    top_selling_products_data = []

    for item in top_selling_products:
        product_id = item['product_id']
        total_quantity = item['total_quantity']

      
        product = Product.objects.get(uid=product_id)
        product_name = product.product_name

        top_selling_products_data.append({
            'product': product_name,
            'total_quantity': total_quantity
        })
    graph = orderitem.objects.filter(
        Q(status='Pending') | Q(status='Successfully Delivered') | Q(status='Cancelled') | Q(status='return')
    ).annotate(
        month=ExtractMonth('order__created_at'),
        category=Cast('product__category', output_field=CharField()) 
    ).values('month', 'status', 'category').annotate(count=Count('id')).values('month', 'status', 'category', 'count')

    delmonthNumber = []
    deltotalOrders = []
    returntotalOrders = []
    canceltotalOrders = []
    pendingtotalOrders = []
    default_value = 0
    total_order_count = defaultdict(int)
    category_orders = defaultdict(int)
    monthNumbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]  
    monthNames = [calendar.month_name[monthNumber] for monthNumber in monthNumbers]

    for g in graph:
        month = g['month']
        status = g['status']
        category = g['category']
        count = g['count']

        if status == 'Successfully Delivered':
            delmonthNumber.append(monthNames[month - 1])
            deltotalOrders.append(count)
        elif status == 'return':
            delmonthNumber.append(monthNames[month - 1])
            returntotalOrders.append(count)
        elif status == 'Cancelled':
            delmonthNumber.append(monthNames[month - 1])
            canceltotalOrders.append(count)
        elif status == 'Pending':
            delmonthNumber.append(monthNames[month - 1])
            pendingtotalOrders.append(count)

        total_order_count[monthNames[month - 1]] += count
        category_orders[category] += count

    
    category_order_counts = dict(category_orders)
    category_order_counts = {str(key): value for key, value in category_order_counts.items()}

    
    return render(request, 'admin_panel/index.html', {
        'delmonthNumber': delmonthNumber,
        'deltotalOrders': deltotalOrders,
        'returntotalOrders': returntotalOrders,
        'canceltotalOrders': canceltotalOrders,
        'pendingtotalOrders': pendingtotalOrders,
        'total_order_count': json.dumps(total_order_count),
        'default_value': default_value,
        'category_order_counts': json.dumps(category_order_counts),'list':list,'new':new,'top_selling_products': top_selling_products_data,
    })

import calendar
def yeargraphical(request):
    list=Order.objects.all()
    new=orderitem.objects.all().order_by('-id')[:5]
    top_selling_products = orderitem.objects.filter(status='Successfully Delivered').values('product_id').annotate(total_quantity=Sum('product_qty')).order_by('-total_quantity')[:10]
    top_selling_products_data = []

    for item in top_selling_products:
        product_id = item['product_id']
        total_quantity = item['total_quantity']

      
        product = Product.objects.get(uid=product_id)
        product_name = product.product_name

        top_selling_products_data.append({
            'product': product_name,
            'total_quantity': total_quantity
        })
    graph = orderitem.objects.filter(
        Q(status='Pending') | Q(status='Successfully Delivered') | Q(status='Cancelled') | Q(status='return')
    ).annotate(
        year=ExtractYear('order__created_at'),
        category=Cast('product__category', output_field=CharField())  
    ).values('year', 'status', 'category').annotate(count=Count('id')).values('year', 'status', 'category', 'count')


    monthNumber = []
    totalOrders = []
    delmonthNumber = []
    deltotalOrders = []
    returnmonthNumber = []
    returntotalOrders = []
    cancelmonthNumber = []
    canceltotalOrders = []
    pendingmonthNumber = []
    pendingtotalOrders = []
    total_order_count = defaultdict(int)
    default_value=0
    category_orders = defaultdict(int)

    

    for g in graph:
        year = g['year']
        status = g['status']
        count = g['count']
        category = g['category']

        if status == 'Successfully Delivered':
            delmonthNumber.append(year)
            deltotalOrders.append(count)
        elif status == 'return':
            returnmonthNumber.append(year)
            returntotalOrders.append(count)
        elif status == 'Cancelled':
            cancelmonthNumber.append(year)
            canceltotalOrders.append(count)
            print("ca",canceltotalOrders)
        elif status == 'Pending':
            pendingmonthNumber.append(year)
            pendingtotalOrders.append(count)

        total_order_count[year] += count
        category_orders[category] += count
    print("archaa",total_order_count)
    total_order_count_dict = dict(total_order_count)
    total_order_count_json = json.dumps(total_order_count_dict)
    category_order_counts = dict(category_orders)
    category_order_counts = {str(key): value for key, value in category_order_counts.items()}


    return render(request, 'admin_panel/index.html', {
        'delmonthNumber': delmonthNumber,
        'deltotalOrders': deltotalOrders,
        'returnmonthNumber': returnmonthNumber,
        'returntotalOrders': returntotalOrders,
        'cancelmonthNumber': cancelmonthNumber,
        'canceltotalOrders': canceltotalOrders,
        'pendingmonthNumber': pendingmonthNumber,
        'pendingtotalOrders': pendingtotalOrders,
        'totalOrders': totalOrders,
        'total_order_count': total_order_count_json,
        'default_value':default_value,
        'category_order_counts': json.dumps(category_order_counts),'list':list,'new':new,'top_selling_products': top_selling_products_data
    })


import calendar
def weekgraphical(request):
    list=Order.objects.all()
    new=orderitem.objects.all().order_by('-id')[:5]
    top_selling_products = orderitem.objects.filter(status='Successfully Delivered').values('product_id').annotate(total_quantity=Sum('product_qty')).order_by('-total_quantity')[:10]
    top_selling_products_data = []

    for item in top_selling_products:
        product_id = item['product_id']
        total_quantity = item['total_quantity']

      
        product = Product.objects.get(uid=product_id)
        product_name = product.product_name

        top_selling_products_data.append({
            'product': product_name,
            'total_quantity': total_quantity
        })
    graph = orderitem.objects.filter(
        Q(status='Pending') | Q(status='Successfully Delivered') | Q(status='Cancelled') | Q(status='return')
    ).annotate(
        week=ExtractWeek('order__created_at'),
        category=Cast('product__category', output_field=CharField())  # Convert UUID to string
    ).values('week', 'status', 'category').annotate(count=Count('id')).values('week', 'status', 'category', 'count')

    delmonthNumber = []
    deltotalOrders = []
    returntotalOrders = []
    canceltotalOrders = []
    pendingtotalOrders = []
    default_value =0
    total_order_count = defaultdict(int)
    category_orders = defaultdict(int)

    for g in graph:
        week = g['week']
        status = g['status']
        count = g['count']
        category = g['category']

        #monthNumber.append(f"Week {week}")
       
        if status == 'Successfully Delivered':
            deltotalOrders.append(count)
            delmonthNumber.append(week)
            
            print("total_order_count")
        elif status == 'return':
            returntotalOrders.append(count)
            delmonthNumber.append(week)
           
        elif status == 'Cancelled':
            canceltotalOrders.append(count)
            
        elif status == 'Pending':
            pendingtotalOrders.append(count)
            delmonthNumber.append(week)
            

        total_order_count[week] += count
        category_orders[category] += count
    print("week",total_order_count)
    total_order_count_dict = dict(total_order_count)
    category_order_counts = dict(category_orders)
    category_order_counts = {str(key): value for key, value in category_order_counts.items()}


    total_order_count_json = json.dumps(total_order_count_dict)

    return render(request, 'admin_panel/index.html', {
        'delmonthNumber': delmonthNumber,
        'deltotalOrders': deltotalOrders,
        'returntotalOrders': returntotalOrders,
        'canceltotalOrders': canceltotalOrders,
        'pendingtotalOrders': pendingtotalOrders,
        'total_order_count': total_order_count_json,
        'default_value':default_value ,
        'category_order_counts': json.dumps(category_order_counts),'list':list,'new':new,'top_selling_products': top_selling_products_data
    })

def order_list(request):
    list=Order.objects.all().order_by('-id')
    context={'list':list}
    return render(request,'admin_panel/index.html',context)

def order_list2(request):
    list=orderitem.objects.all().order_by('-id')
    context={'list':list}
    return render(request,'admin_panel/order.html',context)
def order_cancelled(request,id):
    order = get_object_or_404(orderitem, id=id)
    
    if order.status == 'Pending':
        order.status = 'Cancelled'
        order.save()
    
    return redirect('/admin_panel/order_list2')

def order_update(request,id):
    orders=orderitem.objects.get(id=id)
    context = {} 
    if request.method == 'POST':
        form = OrderUpdateForm(request.POST, instance=orders)
        
        if form.is_valid():
            form.save()
            print("form is saved")
            return redirect('/admin_panel/order_list2')
    else:
        form = OrderUpdateForm(instance=orders)
        context['form'] = form 
    return render(request,'admin_panel/order_update.html',context)

def admin_profile(request):
    user = request.user
    email = user.email
    
    try:
        profile = User.objects.get(id=user.id)
       
    except User.DoesNotExist:
        profile = None

    if request.method == 'POST':
        print("hai")
        profile_form = ProfileForm(request.POST, instance=profile)
        print(profile_form)
        if profile_form.is_valid():
            print("form saved")
            profile = profile_form.save(commit=False)
            profile.save()
            return redirect('/admin_panel/admin_profile')
        else:
            print("not valid")
    else:
        profile_form = ProfileForm(instance=profile)
        
    context = {
        'profile_form': profile_form
    } 
    
    return render(request, 'admin_panel/profile.html', context)
def admin_bank(request):
    print("i am in bank")
    account=Bank_account.objects.all()
    print(account)
    context={'account':account}
    return render(request,'admin_panel/bank.html',context)
def security_settings(request):
        if request.method == 'POST':
            new_password=request.POST.get('new_pass1')
            confirm_password=request.POST.get('new_pass2')
            user=User.objects.get(is_superuser=True)
            user_id=user.id
            
            print(new_password,confirm_password,user_id,'****')
            
            if user_id is None:
                messages.warning(request,'No user id is found')
                return render(request,'admin_panel/admin_security.html')
              
            if new_password != confirm_password:
                messages.warning(request,'Passwords are not equal')
                return redirect('/accounts/changepassword/{token}/')
            
            user_obj=User.objects.get(id= user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            
            return redirect('adminlogin')
        return render(request,'admin_panel/admin_security.html')
    
def salesreport(request):
    orders_list = orderitem.objects.order_by('-id')
    from_date=request.GET.get('from_date')
    to_date=request.GET.get('to_date')
    if from_date and to_date:
        from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
        to_date = datetime.strptime(to_date, '%Y-%m-%d').date()
        orders_list = orders_list.filter(order__created_at__date__gte=from_date, order__created_at__date__lte=to_date)
    paginator = Paginator(orders_list, 5) 
    page = request.GET.get('page')
    orders = paginator.get_page(page)
    total_orders=orders_list.count()
    net_income = 0
    income_orderlist=orders_list.exclude(status__in=[ 'Cancelled', 'return Approved','return'])
    for order in income_orderlist:
        net_income += order.total_price
    
    deliveries=orders_list.filter(status='Successfully Delivered').count()
    canceled=orders_list.filter(Q(status='Cancelled') | Q(status='returned')| Q(status='Return Approved')).count()
    pending=orders_list.filter(status='Pending').count()
    context={'orders':orders,'total_orders':total_orders,'net_income':net_income, 'deliveries':deliveries, 'canceled':canceled, 'pending':pending,}
    return render(request,'admin_panel/salesreport.html',context)
    
    
def adforgottern(request):
        print("hello fo")
        if request.method == 'POST':
                email = request.POST.get('email')
               
            
                if not User.objects.filter(email=email).first():
                        messages.warning(request, 'Not user found with this username.')
                        return redirect('/account/login')
                user_obj = User.objects.get(email = email)
                token = str(uuid.uuid4())
                profile_obj= User.objects.get(email = user_obj)
                profile_obj.forget_password_token = token
                profile_obj.save()
             
                

                subject='your forgot password link'
                message=f'hi , click on the link to reset your password http://127.0.0.1:8000/accounts/changepassword/{token}/'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [user_obj]
                print(recipient_list)
                send_mail(subject, message, email_from, recipient_list)
                messages.success(request, 'An email is sent.')
                return redirect('/accounts/forgottern')
        else:
                form = forgottern_form()
        return render(request,'account/forgottern.html',{'form':form})
def delete_account(request,id):
   
    account=Bank_account.objects.get(id=id)
    account.delete()
    return redirect('security_settings')
def edit_account(request,id):
    orders=Bank_account.objects.get(id=id)
    print(orders.bank)
    if request.method == 'POST':
        profile_form = Bank_account_form(request.POST, instance=orders)
        
        if profile_form.is_valid():
            profile_form.save()
            
            return redirect('order_list2')
    else:
        profile_form = Bank_account_form(instance=orders)
        context={
            'profile_form':profile_form,
            
            } 
    return render(request,'admin_panel/bank_update.html',context)


def productvar_delete(request,uid):
   
    var=ProductAttribute.objects.get(uid=uid)
    var.delete()
    messages.success(request, 'Your product has been deleted.')
    products=Product.objects.all().order_by('-created_at')
    details={'products':products}
    return render(request,'admin_panel/products_manage.html',details)
def orderdetail(request,id):
    oderit = orderitem.objects.filter(id=id) 
    delivered_date = None
    time_difference = None
    
    grand_total = Cart.calculate_grand_total(request.user)
    
    for item in oderit:
        item.progress_percentage = item.calculate_progress_percentage()
        if item.delivered_date is not None:
            item.time_difference = timezone.now().date() - item.delivered_date
            
        print(item.progress_percentage)

    
    context = {'oderit': oderit, 'grand_total': grand_total, 'time_difference': time_difference}
    return render(request, 'admin_panel/orderdetail.html', context)


def approve_return(request,id):
    print("return process")
    order_item = orderitem.objects.get(id=id)
    order = order_item.order
    user = order.user  
  
    user_wallet = Wallet.objects.filter(user=user).first() 
    payment_method = order.payment_mode
    if payment_method in ['razorpay', 'paypal']:
        if user_wallet:
            user_wallet.amount += order_item.total_price
            user_wallet.save()
            order_item.status='Return Approved'
            order_item.save()
        else:
            user_wallet = Wallet.objects.create(user=user, amount=order_item.total_price)  
    else:
            order_item.status='Return Approved'
            order_item.save()
    return redirect('/admin_panel/order_list2')