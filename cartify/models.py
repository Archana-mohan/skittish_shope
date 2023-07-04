from django.db import models
from django.utils.text import slugify
from base.models import BaseModel
from django.utils.html import mark_safe
from accounts.models import User
from products.models import *
from userprofile.models import *

class Coupon(models.Model):
    coupon_code= models.CharField(max_length=50)
    is_expired= models.BooleanField(default=False)
    discount_price= models.IntegerField(default=100)
    minimum_amount=models.IntegerField(default=500)
    is_used = models.BooleanField(default=False,null=True)
    
    def __str__(self):
        return self.coupon_code


class Cart(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    coupon= models.ForeignKey(Coupon,on_delete=models.SET_NULL,blank=True,null=True)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    productattr=models.ForeignKey(ProductAttribute, on_delete=models.CASCADE,null=True)
    product_qty=models.IntegerField(null=False,blank=False)
    product_price=models.FloatField(null=False,blank=False,default=False)
    size = models.CharField(max_length=100,default=False)
    color= models.CharField(max_length=100,default=False)
    total_price=models.FloatField(null=False,blank=False,default=False)
    created_at=models.DateTimeField(auto_now_add=True)
   
    
    @classmethod
    def calculate_grand_total(cls,user):
        user_wallet = Wallet.objects.get(user=user)
        cart_items = Cart.objects.filter(user=user)
        grand_total = 0
     
        for cart_item in cart_items:
            total_product_price = cart_item.product_qty * cart_item.product_price
            if cart_item.coupon:
                total_product_price -= cart_item.coupon.discount_price
            grand_total += total_product_price
        if user_wallet.discount:
            grand_total -= user_wallet.discount
        return grand_total
   
    

    @classmethod
    def get_coupon(cls, user):
        """
        Get the coupon associated with the user's cart, if any.
        """
        try:
            print("this is get coupon")
            carts = Cart.objects.filter(user=user) 
            print(carts)
            for cart in carts:
                print(cart.coupon_id)
                return cart.coupon_id
        except cls.DoesNotExist:
            return None
