from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import CustomUserForm,signinuserForm,forgottern_form,change_form,otp_form
from django.http import HttpResponse
from .models import User
from .helpers import *
from django.conf import settings
import random
from django.contrib.auth import authenticate,login,logout
from .base import *
import uuid
from userprofile.models import *
from django.core.mail import send_mail
from django.contrib.auth.views import LoginView
from django.views.decorators.cache import never_cache

from django.contrib.auth import get_user_model
from cartify.models import *

# Create your views here.

@never_cache
def signuppage(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        if request.user.is_otp_verified:
            return redirect('/accounts/login')
        else:
            return redirect('/accounts/logout')

    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            referral_code = request.GET.get('referral_code')
           
            if referral_code:
                referred_user = User.objects.filter(referral_code=referral_code).first()
                print("Referred User:", referred_user)
                if referred_user:
                    user_wallet = Wallet.objects.filter(user=referred_user).first()
                    if user_wallet:
                        user_wallet.discount += 100  # Apply discount to the referring user's cart
                        user_wallet.save()
            
            user.save()
            return redirect('/')
    else:
        form = CustomUserForm()

    return render(request, 'account/signups.html', {'form': form})


@never_cache
def loginpage(request):  
        if request.user.is_authenticated and not request.user.is_superuser:
               
                if request.user.is_otp_verified:
                       
                        if request.user.is_blocked:
                                
                                messages.warning(request,"Account Blocked !!")
                                return redirect('/accounts/logout')
                        else:
                                return redirect('/')
                else:
                         return redirect('/accounts/logout')

        if request.method=='POST':
               
                email=request.POST.get('email')
                mobile='+91'+request.POST.get('mobile')
                
                
                password=request.POST.get('password')
                
                user=authenticate(request,email=email,password=password)
                
                if user is not None:
                        
                        login(request,user)
                        otp=str(random.randint(1000,9999))
                        profile=User.objects.get(mobile=mobile)
                        profile.otp=otp
                        profile.save()
                        
                        obj=MessaHandler(mobile,otp)
                        obj.send_otp_on_mobile()
                      
                        request.session['mobile'] = mobile
                        if request.user.is_blocked:
                                messages.warning(request,"You are blocked !!") 
                                return redirect('/accounts/login')
                        
                        else:
                                return redirect('/accounts/otp_varificaton')
                
                else:
                    messages.warning(request,"Incorrect !!")    
       
             
        form = signinuserForm()  
        print('c')      
                
        return render(request, 'account/login.html',{'form':form})
@never_cache
def otp_varificaton(request):
        print('good')
        if request.user.is_authenticated and not request.user.is_superuser:
                if request.user.is_otp_verified:
                        if request.user.is_blocked:
                              
                                return redirect(request,'accounts/login')
                        else:
                                return redirect('/')
                                
        mobile=request.session['mobile']
       
        context={'mobile':mobile}
        if request.method == 'POST':
                otp=request.POST.get('otp')
               
                profile=User.objects.filter(mobile=mobile).first()
                
                if otp == profile.otp:
                        if profile.is_authenticated and not profile.is_superuser:
                                profile.is_otp_verified=True
                                
                                profile.save()
                                return redirect('/')
                        messages.success(request,'Successfully registered')
                        return redirect('/accounts/login')
                else:
                        messages.warning(request,'Incorrect OTP')
                        form = otp_form()
                        return render(request,'account/otp_valid.html')
        else:
                form = otp_form()
        return render(request,'account/otp_valid.html', {'form':form})
@never_cache   
def logoutpage(request):
    request.user.is_otp_verified=False
   
    request.user.save()
    logout(request)
    return redirect('/accounts/login')
@never_cache
def forgottern(request):
        if request.method == 'POST':
                email = request.POST.get('email')
                print(email)
            
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
                
                send_mail(subject, message, email_from, recipient_list)
                messages.success(request, 'An email is sent.')
                return redirect('/accounts/forgottern')
        else:
                form = forgottern_form()
        return render(request,'account/forgottern.html',{'form':form})
@never_cache
def changepassword(request,token):
        profile_obj=User.objects.filter(forget_password_token=token).first()
       
       # context = {'user_id':profile_obj.id}
        if request.method == 'POST':
            new_password=request.POST.get('new_password')
            confirm_password=request.POST.get('confirm_password')
            user_id=request.POST.get('first_name')
            

            if user_id is None:
                messages.warning(request,'No user id is found')
                return redirect('/accounts/changepassword/{token}/')
            
            if new_password != confirm_password:
                messages.warning(request,'Passwords are not equal')
                return redirect('/accounts/changepassword/{token}/')
            
            user_obj=User.objects.get(first_name= user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            return redirect('/accounts/login')
        else:
                 form = change_form()
        
        return render(request,'account/changepassword.html',{'form':form})

