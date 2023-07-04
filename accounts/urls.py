
from django.urls import path,include
from .import views

urlpatterns = [ 
    path('login', views.loginpage,name='login'),
    path('signup', views.signuppage,name='signup'),
    path('logout', views.logoutpage,name='logout'),
    path('otp_varificaton', views.otp_varificaton,name='otp_varificaton'),
    path('forgottern',views.forgottern,name='forgottern'),
    path('changepassword/<token>/',views.changepassword,name='changepassword'),
    path('gender_view/ <str:uid>',include('products.urls')),
    path('category_view/ <str:uid>',include('products.urls')),


]