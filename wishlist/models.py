from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from base.models import BaseModel
from django.utils.html import mark_safe
from products.models import *
from accounts.models import *

class Wishlist(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    productattr=models.ForeignKey(ProductAttribute, on_delete=models.CASCADE,null=True)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    product_price=models.FloatField(null=True,blank=False)
    product_qty=models.IntegerField(null=True,blank=False)
    created_at=models.DateTimeField(auto_now_add=True,null=True)