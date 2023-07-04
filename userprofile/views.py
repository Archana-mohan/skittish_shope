from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.cache import never_cache
from django.contrib import messages
from accounts.models import User
from products.models import *
from .forms import *
from .models import *
from django.shortcuts import get_object_or_404

def addaddress(request):
    try:
        user_id = request.user.id
    except AttributeError:
        user_id = None
    
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address_obj = form.save(commit=False)
            address_obj.user_id = user_id

            # Check if the address already exists for the user
            existing_addresses = Address.objects.filter(user_id=user_id, 
                                            address__iexact=address_obj.address,
                                            username__iexact=address_obj.username)

            if existing_addresses:
                messages.warning(request, "Address already exists!")
                return redirect('/userprofile/addaddress')

            address_obj.save()
            messages.success(request, "Address added successfully!")
            return redirect('/userprofile/address')
    else:
        form = AddressForm()

    return render(request, 'userprofile/addaddress.html', {'form': form})
def address(request):
    address=Address.objects.filter(user=request.user)
    context={'address':address}
    return render(request,'userprofile/useraddress.html',context)
def user_address(request):
    address=Address.objects.filter(user=request.user)
    context={'address':address}
    return render(request,'userprofile/useraddress.html',context)
def address_delete(request,uid):
    print(uid)
    user=Address.objects.get(uid=uid)
    user.delete()
    details={'user':user}
    return redirect('/userprofile/address')

def user_profile(request):
    user = request.user
    email = user.email
    
    try:
        profile = User.objects.get(id=user.id)
        print("profile sdd",profile)
    except User.DoesNotExist:
        profile = None

    if request.method == 'POST':
        print("hai")
        profile_form = AddprForm(request.POST, instance=profile)
        print(profile_form)
        if profile_form.is_valid():
            print("form saved")
            profile = profile_form.save(commit=False)
            
            profile.save()
            return redirect('/userprofile/user_profile')
        else:
            print("not valid")
    else:
        profile_form = AddprForm(instance=profile)
        
    context = {
        'profile_form': profile_form
    } 
    
    return render(request, 'userprofile/address.html', context)
def edit_address(request,uid):
    address=Address.objects.get(uid=uid)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        
        if form.is_valid():
            form.save()
            
            return redirect('/userprofile/user_profile')
    else:
        form = AddressForm(instance=address)
        context={
            'form':form,
            'image_form':form
            } 
    return render(request,'userprofile/address_update.html',context)



def settings(request):
    user_wallet = Wallet.objects.get(user=request.user)
    context={'user_wallet':user_wallet}
    if request.method == 'POST':
            new_password=request.POST.get('new_pass1')
            confirm_password=request.POST.get('new_pass2')
            user=request.user
            user_id=user.id
            print(user_id)
            print(new_password,confirm_password,user_id,'****')
            
            if user_id is None:
                messages.warning(request,'No user id is found')
                return redirect('/userprofile/user_profile')
              
            if new_password != confirm_password:
                messages.warning(request,'Passwords are not equal')
                return redirect('/userprofile/user_profile')
            
            user_obj=User.objects.get(id= user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            
            return redirect('/')
    return render(request,'userprofile/settings.html',context)