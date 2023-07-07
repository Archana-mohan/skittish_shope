from django.db import models
from django.utils.text import slugify
from base.models import BaseModel
from django.utils.html import mark_safe
from accounts.models import User
from django.db.models import Max,Min,Count,Avg,Aggregate

# Create your models here.
class front_image(models.Model):
    img=models.ImageField(upload_to="front_image")
    img2 = models.ImageField(upload_to="front_image", default='default_image.jpg', null=True)
    heading=models.CharField(max_length=300,null=True)
    categ=models.CharField(max_length=300,null=True)
    price=models.CharField(max_length=300,null=True)

class gender(BaseModel):
    gender_name = models.CharField(max_length=100,null=True)
    slug = models.SlugField(unique=True , null=True , blank=True)
    gender_image = models.ImageField(upload_to="catgories")
      
    def save(self , *args , **kwargs):
        self.slug = slugify(self.gender_name)
        super(gender ,self).save(*args , **kwargs)


    def __str__(self) -> str:
        return self.gender_name


class Category(BaseModel):
    category_name = models.CharField(max_length=100,null=True)
    slug = models.SlugField(unique=True , null=True , blank=True)
    status=models.BooleanField(default=False, help_text="0=default,1=Hidden")
    category_image = models.ImageField(upload_to="catgories")
    offer = models.FloatField(null=True, blank=True)
    
    
    def save(self, *args, **kwargs):
        super(Category, self).save(*args, **kwargs)
        if self.offer:
            products = self.product.all()
            for product in products:
                product_attributes = product.productattribute_set.all()
                for attribute in product_attributes:
                    percentage_discount = float(self.offer) / 100
                    attribute.selling_price = attribute.selling_price - (attribute.selling_price * percentage_discount)
                    attribute.save()
                    print(f"Updated selling price for ProductAttribute {attribute.uid}: {attribute.selling_price}")

    def save(self , *args , **kwargs):
        self.slug = slugify(self.category_name)
        super(Category ,self).save(*args , **kwargs)

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.category_image.url))

    def __str__(self) -> str:
        return self.category_name


class ColorVariant(BaseModel):
    color_name = models.CharField(max_length=100,null=True)
    color_code=models.CharField(max_length=100,default=False,null=True)
  
  

    def color_bg(self):
        return mark_safe('<div style="width:10px; height:10px; background-color:%s"></div>' % (self.color_code))

    def __str__(self) -> str:
        return self.color_name

class SizeVariant(BaseModel):
    size_name = models.CharField(max_length=100)
   
    
    def __str__(self) -> str:
        return self.size_name

class Product(BaseModel):
    product_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True  , null=True , blank=False)
    gender= models.ForeignKey(gender , on_delete=models.CASCADE , related_name="products")
    category = models.ForeignKey(Category , on_delete=models.CASCADE , related_name="products")
    trending=models.BooleanField(default=False,help_text="0=default, 1=Hidden")
    small_desription = models.TextField(default=False)
    Detail_desription = models.TextField(default=False)
    is_available=models.BooleanField(default=False)
    status=models.BooleanField(default=False, help_text="0=default,1=Hidden")
    meta_title=models.CharField(max_length=150,default=False,blank=False)
    meta_discription=models.CharField(max_length=150,default=False,blank=False)
    meta_keyword=models.CharField(max_length=150,default=False,blank=False)
    tag=models.CharField(max_length=150,default=False,blank=False)
    created_at=models.DateTimeField( auto_now_add=True)
    def save(self , *args , **kwargs):
        self.slug = slugify(self.product_name)
        super(Product ,self).save(*args , **kwargs)


    def __str__(self) -> str:
        return self.product_name

class ProductAttribute(BaseModel):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=False,blank=False)
    sizevariant= models.ForeignKey(SizeVariant,on_delete=models.CASCADE,null=True)
    colorVariant=models.ForeignKey(ColorVariant,on_delete=models.CASCADE)
    orginal_price=models.FloatField(default=False,blank=False)
    selling_price=models.FloatField(default=False,blank=False)
    
    def save(self, *args, **kwargs):
        category_offer = self.product.category.offer
        if category_offer is not None:
            percentage_discount = float(category_offer) / 100
            self.selling_price = self.orginal_price - (self.orginal_price * percentage_discount)
        super(ProductAttribute, self).save(*args, **kwargs)
        print(f"Updated selling price for ProductAttribute {self.uid}: {self.selling_price}")


    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self. product.product_name
    
class ProductImage(BaseModel):
    product_attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE , related_name="product_images",null=True)
    image = models.ImageField(upload_to="product",null=True)


    def image_tag(self):
        try:
            return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
        except:
            return 'No Image Found'
        
RATING = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
)

class Review(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.IntegerField(choices=RATING)
    added_at=models.DateTimeField( auto_now_add=True,null=True)

    class Meta:
        verbose_name_plural = 'Reviews'
    def get_average_rating(self):
        return self.review_set.aggregate(avg_rating=Avg('rating'))['avg_rating']
