
from django.urls import path,include
from .import views

urlpatterns = [ 
    path('add_cart', views.add_cart,name='add_cart'),
    path('cart',views.cart,name='cart'),
    path('delete_cart',views.delete_cart,name='delete_cart'),
    path('update_cart',views.update_cart,name='update_cart'),
    path('apply_coupon',views.apply_coupon,name='apply_coupon'),
    path('checkout',views.checkout,name='checkout'),
    path('coupon',views.coupon,name='coupon'),
    path('cartempty',views.cartempty,name='cartempty'),
]
