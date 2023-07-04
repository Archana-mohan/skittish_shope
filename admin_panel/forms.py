from django.contrib.auth.forms import UserCreationForm  

from accounts.models import User
from products.models import *
from cartify.models import *
from oders.models import *
from admin_panel.models import *
from django import forms
from django.forms.models import inlineformset_factory
from bootstrap_datepicker_plus.widgets import DatePickerInput

class ProductUpdateForm(forms.ModelForm):
    product_name=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control my-2','placeholder':'Name of Product' }))
    gender=forms.ModelChoiceField(queryset=gender.objects.all(),widget=forms.Select(attrs={'class': 'form-control'}))
    category=forms.ModelChoiceField(queryset=Category.objects.all(),widget=forms.Select(attrs={'class': 'form-control'}))
    small_desription=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control my-2','placeholder':'small description'}))
    Detail_desription=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control my-2','placeholder':'Detail Description'}))
    status=forms.BooleanField(required=False)
    trending=forms.BooleanField(required=False)
    meta_title=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control my-2','placeholder':'Meta title'}))
    meta_keyword=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control my-2','placeholder':'Meta Keywords'}))
    meta_discription=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control my-2','placeholder':'Meta Descritption'}))
    tag=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control my-2','placeholder':'tag'}))
    class Meta:
        model = Product
        fields =['product_name','gender','category','small_desription','Detail_desription','tag','status','trending','meta_title',
                 'meta_keyword','meta_discription'
                 
                 ]

class ProductImageForm(forms.ModelForm):
    image = forms.ImageField()

    class Meta:
        model=ProductImage
        fields=['image']


class ProductVariantForm(forms.ModelForm):
    colorVariant=forms.ModelChoiceField(queryset=ColorVariant.objects.all(),widget=forms.Select(attrs={'class': 'form-control'}))
    sizevariant=forms.ModelChoiceField(queryset=SizeVariant.objects.all(),widget=forms.Select(attrs={'class': 'form-control'}))
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}),initial=0)
    orginal_price=forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control my-2','placeholder':'Original Price'}))
    selling_price=forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control my-2','placeholder':'Selling Price'}))
    
    class Meta:
        model=ProductAttribute
        fields=['colorVariant', 'sizevariant',  'orginal_price','selling_price','quantity' ]


ProductVariantFormSet = inlineformset_factory(
        Product, ProductAttribute, form=ProductVariantForm, extra=3, can_delete=True
    )

ProductImageFormSet = inlineformset_factory(
       ProductAttribute, ProductImage, form=ProductImageForm, extra=3, can_delete=True
    ) 


class CategoryUpdateForm(forms.ModelForm):
    category_name=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control my-2','placeholder':'Name of Category' }))
    slug=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control my-2','placeholder':'Name of Slug' }))
    category_image= forms.ImageField()
    offer = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control my-2', 'placeholder': 'Offer'}), required=False)

    class Meta:
        model = Category
        fields =['category_name','slug','category_image','offer'  
        ]
        widgets = {
            'category_image': forms.ClearableFileInput(attrs={'multiple': True},),
        }
    
class OrderUpdateForm(forms.ModelForm):
    
    oderstatus = (
        ('Pending', 'Pending'),
        ('Out For Shipping', 'Out For Shipping'),
        ('Successfully Delivered', 'Successfully Delivered')
    )
    status = forms.ChoiceField(choices=oderstatus, initial='Pending')
    message=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control my-2','placeholder':'Message'}))
    delivered_date = forms.DateField(
    widget=DatePickerInput(
        options={
            'format': 'yyyy-mm-dd',  # Set the desired format here
            # Other options...
        }
    )
)
    class Meta:
        model = orderitem
        fields =['status','message','delivered_date'   
        ]
           
        
class CouponUpdateForm(forms.ModelForm):
    coupon_code=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control my-2','placeholder':'Name of Coupon' }))
    is_expired=forms.BooleanField(required=False)
    discount_price= forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control my-2','placeholder':'Discount Price'}))
    minimum_amount= forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control my-2','placeholder':'Minimum Amount'}))

    class Meta:
        model = Coupon
        fields =['coupon_code','is_expired','discount_price','minimum_amount' 
        ]
        
class ProfileForm(forms.ModelForm):
    first_name=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control my-2 form-control-lg','placeholder':'Enter First Name' }))
    last_name=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control my-2 form-control-lg','placeholder':'Enter Last Name' }))
    email=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control my-2 form-control-lg','placeholder':'Enter email address' }))
    mobile=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control my-2 form-control-lg','placeholder':'Enter Your phonenumber' }))
   
    class Meta:
        model = User
        fields =['first_name','last_name','email','mobile']
        
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Exclude password fields from form validation
        self.fields.pop('password1', None)
        self.fields.pop('password2', None)
        
class forgottern_form(UserCreationForm):
    email=forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control my-2','placeholder':'Enter Email' }))
    
    class Meta:
        model = User
        fields=['email']
        
class Bank_account_form(UserCreationForm):
    account_name=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control my-2','placeholder':'Account Name' }))

    Bank=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control my-2','placeholder':'Bank'}))
    Branch=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control my-2','placeholder':'Branch'}))
    IFSC=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control my-2','placeholder':'IFSC'}))
    account_number=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control my-2','placeholder':'IFSC'}))
    upi=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control my-2','placeholder':'IFSC'}))
    class Meta:
        model =Bank_account
        fields =['account_name','Bank','Branch','IFSC','account_number','upi']