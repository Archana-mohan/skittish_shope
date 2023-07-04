from django.conf import settings
from django.db import models
from accounts.models import User

class Bank_account(models.Model):
   
    account_name= models.CharField(max_length=50)
    bank= models.CharField(max_length=50)
    branch= models.CharField(max_length=50)
    IFSC= models.CharField(max_length=50)
    acccount_number= models.CharField(max_length=50)
    Upi= models.CharField(max_length=50)
    
    
    
    def __str__(self):
        return self.account_name