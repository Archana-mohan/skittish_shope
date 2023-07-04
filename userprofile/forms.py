from django.contrib.auth.forms import UserCreationForm  
from accounts.models import User
from .models import Address
from django import forms

class AddressForm(forms.ModelForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control my-2 form-control-lg','placeholder':'Enter Username' }))
    address=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control my-2 form-control-lg','placeholder':'Enter Address' }))
    city=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control my-2 form-control-lg','placeholder':'Enter Your City' }))
    state=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control my-2 form-control-lg','placeholder':'Enter your State' }))
    country=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control my-2 form-control-lg','placeholder':'Enter Your Country' }))
    pincode=forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control my-2 form-control-lg','placeholder':'Enter Pincode' }))
    
    class Meta:
        model = Address
        fields =['username','address','city','state','country','pincode']
        
class AddprForm(forms.ModelForm):
    first_name=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control my-2 form-control-lg','placeholder':'Enter First Name' }))
    last_name=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control my-2 form-control-lg','placeholder':'Enter Last Name' }))
    email=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control my-2 form-control-lg','placeholder':'Enter email address' }))
    mobile=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control my-2 form-control-lg','placeholder':'Enter Your phonenumber' }))
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    class Meta:
        model = User
        fields =['first_name','last_name','email','mobile','image']
        
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Exclude password fields from form validation
        self.fields.pop('password1', None)
        self.fields.pop('password2', None)