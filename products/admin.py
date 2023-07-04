from csv import list_dialects
from django.contrib import admin
from .models import *

admin.site.register(front_image)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(ProductImage)
admin.site.register(SizeVariant)
admin.site.register(gender)

class ProductAttributeProductImageInline(admin.TabularInline):
    model =ProductImage
    
class ProductProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
      
@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ['product']
    inlines = [ProductAttributeProductImageInline]   


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name']
    inlines = [ProductProductAttributeInline]
    
@admin.register(ColorVariant)
class ColorVariantAdmin(admin.ModelAdmin):
    list_display = ['color_name' ]
    

    


