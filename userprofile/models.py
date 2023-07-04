from django.db import models
from django.utils.text import slugify
from base.models import BaseModel
from django.utils.html import mark_safe
from accounts.models import User
from products.models import *
from django.contrib.auth.models import AbstractUser
from accounts.manager import UserManager
from django.utils import timezone

COUNTRY_CHOICES = (
    ('US', 'United States'),
    ('IN', 'India'),
    ('UK', 'United Kingdom'),
    # Add more countries as needed
    )

class Address(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    username=models.CharField( max_length=150,null=True)
    address=models.TextField()
    city=models.CharField( max_length=150,null=False)
    state=models.CharField( max_length=150,null=False)
    country=models.CharField( max_length=150,null=False,choices=COUNTRY_CHOICES)
    pincode=models.CharField( max_length=150,null=False)
    created_at=models.DateTimeField( auto_now=True)
    
    def __str__(self):
        return f"{self.city}, {self.state}, {self.country} - {self.pincode}"
    
class Wallet(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount=models.FloatField(default=False,blank=False)
    discount=discount = models.FloatField(default=0) 
    
