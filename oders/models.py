from django.db import models
from django.utils.text import slugify
from base.models import BaseModel
from django.utils.html import mark_safe
from accounts.models import User
from products.models import *
from cartify.models import *
from userprofile.models import *
from django import template
from datetime import timedelta
from django.utils import timezone



register = template.Library()


class Order(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    address=models.ForeignKey(Address,on_delete=models.SET_NULL,blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    total_price=models.FloatField(null=False,blank=False,default=False)
    payment_mode=models.CharField(max_length=100,default=False)
    payment_id=models.CharField(max_length=100,default=False)
    oderstatus=(('Pending','Pending'),('Out For Shipping','Out For Shipping'),('Successfully Delivered','Successfully Delivered'),('Shipped','Shipped'),('Return Approved','Return Approved'))
    status=models.CharField(max_length=100,choices=oderstatus,default='Pending')
    message=models.TextField(null=True,blank=True)
    coupon= models.ForeignKey(Coupon,on_delete=models.SET_NULL,blank=True,null=True)
    tracking_number=models.CharField(max_length=100,default=False)
   
    
    def __str__(self):
        if self.id is not None and self.tracking_number is not None:
            return f'{self.id}-{self.tracking_number}'
        else:
            return ''
class orderitem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    productattr=models.ForeignKey(ProductAttribute, on_delete=models.CASCADE,null=True)
    product_price=models.FloatField(null=True,blank=False,default=False)
    total_price=models.FloatField(null=True,blank=False,default=False)
    product_qty=models.IntegerField(null=False,blank=False) 
    size = models.CharField(max_length=100,default=False)
    color= models.CharField(max_length=100,default=False)
    oderstatus=(('Pending','Pending'),('Out For Shipping','Out For Shipping'),('Successfully Delivered','Successfully Delivered'),('Shipped','Shipped'),('Return Approved','Return Approved'))
    status=models.CharField(max_length=100,choices=oderstatus,default='Pending',null=True)
    return_reason = models.TextField(blank=True, null=True)
    delivered_date = models.DateField( null=True)
  
    
    
    def __str__(self):
        return '{} {}'.format(self.order.id, self.order.tracking_number,self.status)
    
    
    def calculate_progress_percentage(self):
       
        total_statuses = 3  # Total number of possible statuses
        completed_statuses = {'Pending','Out For Shipping', 'Successfully Delivered'}  # Set of completed statuses

        if self.status =='Pending':
            return 25
        if self.status =='Shipped':
            return 50
        elif self.status == 'Successfully Delivered':
            return  100
        elif self.status == 'Cancelled':
            return  0
        else:
            return ''
    
     
    def progressColor(self):
        if self.status == 'Successfully Delivered':
            return 'green'
        elif self.status == 'Pending':
            return 'blue'
        elif self.status == 'Shipped':
            return 'info'
        elif self.status == 'Cancelled':
            return 'red'
        else:
            return ''
    def get_estimated_delivery_date(self):
        return self.order.created_at + timedelta(days=3)