from django.shortcuts import render
from .models import *
from django.http import HttpResponse
from accounts.models import User
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Max,Min,Count,Avg
from cartify.models import *
from wishlist.models import *
from django.views.decorators.http import require_GET
from django.db.models import Count
from django.db.models import Q
from django.db.models.functions import Cast
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.db.models import F
# Create your views here.
@never_cache
def indexpage(request):
    print("hello")
    data=front_image.objects.all()
    gen=gender.objects.all()
    cat=Category.objects.filter(status=0)
    new=Product.objects.filter(status=0).annotate(review_count=Count('review')).order_by('-created_at')[:4]
    new = new.annotate(average_rating=Avg('review__rating'))
    print(new)
    all_products=Product.objects.filter(status=0).annotate(review_count=Count('review'))
    images=ProductImage.objects.all()
    all_colors=ProductAttribute.objects.all().values('colorVariant') 
    all_products = all_products.annotate(average_rating=Avg('review__rating'))
    
    print(data)
    iterator = range(1, 6)
    
  
    count= Product.objects.filter(status=0).annotate(review_count=Count('review'))
    print("the count",count)
    
    product_attributes = ProductAttribute.objects.all()

    for product_attribute in product_attributes:
        # Access the offer field of the associated category
        category_offer = product_attribute.product.category.offer

        if category_offer is not None:
            # Apply the offer discount calculation
            percentage_discount = float(category_offer) / 100
            product_attribute.selling_price = product_attribute.orginal_price - (product_attribute.orginal_price * percentage_discount)
            product_attribute.save()
            print(f"Updated selling price for ProductAttribute {product_attribute.uid}: {product_attribute.selling_price}")
        else:
            print(f"No offer available for ProductAttribute {product_attribute.uid}")
    
    if request.user.is_authenticated and not request.user.is_superuser:
            if request.user.is_otp_verified and not request.user.is_blocked:
                    cart=Cart.objects.filter(user=request.user)
                    wishlist=Wishlist.objects.filter(user=request.user)
                    print('hai')
                    return render(request,'account/firstpage.html',{'gen':gen,'data':data, 'cat':cat, 'new':new,'all_products':all_products,'all_colors':all_colors,'images':images,'cart':cart,'wishlist':wishlist,'iterator':iterator})
            else:
                    print('archana')
                    return render(request,'account/index.html',{'gen':gen,'data':data, 'cat':cat, 'new':new,'all_products':all_products})
    else:
        print("entha")
        return render(request,'account/index.html',{'gen':gen,'data':data, 'cat':cat, 'new':new,'all_products':all_products})

            

def gender_view(request,uid):
    print(uid)
   
    all_gender=gender.objects.all()
    all_catdisp=Category.objects.all()
    all_color=ColorVariant.objects.all()
    all_size=SizeVariant.objects.all()
    minMaxprice=ProductAttribute.objects.aggregate(Min('selling_price'),Max('selling_price'))
    if gender.objects.get(uid=uid):
        Gender=gender.objects.get(uid=uid)
        products=Product.objects.filter(gender=Gender)
        print(Gender)
        context={'products':products,
                'all_gender':all_gender,
                'all_catdisp':all_catdisp,
                'all_color':all_color,
                'all_size':all_size,
                'minMaxprice':minMaxprice}        
    return render(request,'account/product_list.html',context)

def category_view(request,uid):
     
    all_gender=gender.objects.all()
    all_catdisp=Category.objects.all()
    all_color=ColorVariant.objects.all()
    all_size=SizeVariant.objects.all()
    minMaxprice=ProductAttribute.objects.aggregate(Min('selling_price'),Max('selling_price'))
    if Category.objects.get(uid=uid):
        cat=Category.objects.get(uid=uid)
        products=Product.objects.filter(category=cat)
    context={'products':products,
                'all_gender':all_gender,
                'all_catdisp':all_catdisp,
                'all_color':all_color,
                'all_size':all_size ,
                'minMaxprice':minMaxprice}        
    return render(request,'account/product_list.html',context)

def product_list(request):
    total_data=Product.objects.count()
    products=Product.objects.all()
    all_gender=gender.objects.all()
    all_catdisp=Category.objects.all()
    all_color=ColorVariant.objects.all()
    all_size=SizeVariant.objects.all()
    context={'products':products,
                'all_gender':all_gender,
                'all_catdisp':all_catdisp,
                'all_color':all_color,
                'total_data':total_data,
                'all_size':all_size }        
    return render(request,'account/product_list.html',context)

def all_products(request):
    total_data=Product.objects.count()
    products=Product.objects.all().order_by('-uid')[:1]
    all_gender=gender.objects.all()
    all_catdisp=Category.objects.all()
    all_color=ColorVariant.objects.all()
    all_size=SizeVariant.objects.all()


    # Rest of your view function
    minMaxprice=ProductAttribute.objects.aggregate(Min('selling_price'),Max('selling_price'))
    print(minMaxprice)
    context={'products':products,
                'all_gender':all_gender,
                'all_catdisp':all_catdisp,
                'all_color':all_color,
                'all_size':all_size ,
                'total_data':total_data,
                #'images':images,
                'minMaxprice':minMaxprice
                }        
    return render(request,'account/product_list.html',context)

def filter_data(request):
    colors=request.GET.getlist('color[]')
    print(colors)
    sorting=request.GET.getlist('sorting[]')
    print(sorting)
    genders=request.GET.getlist('gender[]')
    print(genders)
    categories=request.GET.getlist('category[]')
    sizes=request.GET.getlist('size[]')
    minPrice=request.GET['minPrice']
    maxPrice=request.GET['maxPrice']
    allproducts=Product.objects.all().order_by('-uid')
    allproducts=allproducts.filter(productattribute__selling_price__gte=minPrice).distinct()
    allproducts=allproducts.filter(productattribute__selling_price__lte=maxPrice).distinct()
    if len(genders)>0:
        allproducts=allproducts.filter(gender__uid__in=genders)
    if len(categories)>0:
        allproducts=allproducts.filter(category__uid__in=categories)
    if len(sizes)>0:
        allproducts=allproducts.filter(productattribute__sizevariant__uid__in=sizes)
    if len(colors)>0:
        allproducts=allproducts.filter(productattribute__colorVariant__uid__in=colors)
    if 'A' in sorting:
        print('hai')
        allproducts=allproducts.filter().order_by('-created_at')[:3]
        print(allproducts)
    if 'Z' in sorting:
        print('hai')
        allproducts=allproducts.filter(tag='Trending').order_by('-product_name')
        print(allproducts)
    if 'L' in sorting:
        allproducts = allproducts.filter().annotate(min_selling_price=Min('productattribute__selling_price'))
        print('hai')
        allproducts= allproducts.order_by('min_selling_price')
        print(allproducts)
    if 'H' in sorting:
        print('hai')
        allproducts = allproducts.filter().annotate(min_selling_price=Max('productattribute__selling_price'))
        allproducts= allproducts.order_by('-min_selling_price')
        print(allproducts)
        
    t=render_to_string('ajax/product_list.html',{'data':allproducts})
    return JsonResponse({'data':t})
def product_detail(request,uid):
    if Product.objects.filter(uid=uid):
        product=Product.objects.filter(uid=uid)
        produ=Product.objects.get(uid=uid)
        related_product=Product.objects.filter(category=produ.category,gender=produ.gender).exclude(uid=uid)
        print("relatedproduct",related_product)
        sizes=ProductAttribute.objects.filter(product=produ).values('sizevariant__size_name','sizevariant__uid','selling_price','colorVariant__uid','quantity').distinct()
        print(sizes)
        colors = ProductAttribute.objects.filter(product=produ).values('uid', 'colorVariant__uid', 'colorVariant__color_code').distinct('colorVariant__uid', 'colorVariant__color_code')

        print("id",colors)
        #colors=ProductAttribute.objects.filter(product=produ).values('colorVariant__uid','sizevariant__size_name','sizevariant__uid','selling_price','uid').distinct()
        orginal=ProductAttribute.objects.filter(product=produ).values('orginal_price')
        minMaxPrice=ProductAttribute.objects.aggregate(Min('selling_price'),Max('selling_price'))
        selling=ProductAttribute.objects.filter(product=produ).values('selling_price')
        context = {}
        reviews_on_product = Review.objects.filter(product=produ).order_by('-added_at')
        
        reviews_count = reviews_on_product.count()
        print("reviews_count",reviews_on_product)
        item_count = 0

        if request.user.is_authenticated:
            review_by_user = reviews_on_product.filter(user=request.user)
            context['review_by_user'] = review_by_user

        context['item_count'] = item_count
        context['reviews_on_product'] = reviews_on_product
        
        iterator = range(1, 6)
        print(iterator )
        average_rating = Review.get_average_rating(produ)
        rounded_average_rating = round(average_rating, 1) if average_rating is not None else 0.0
        print(rounded_average_rating)
        
        context={'data':product,'sizes':sizes,'orginal':orginal,'selling':selling,'colors':colors,'minMaxPrice':minMaxPrice,'related_product':related_product,'rounded_average_rating':rounded_average_rating,'reviews_count': reviews_count,'reviews_on_product':reviews_on_product,'iterator': iterator}
    return render(request,'account/product.html',context)




@require_GET


def search(request):
    query = request.GET.get('q', '')
    keywords = query.split()  

    products = Product.objects.filter(status=0)
    filtered_products = []

    for product in products:
        meta_keywords = product.meta_keyword.lower()
        keyword_matched = True

        for keyword in keywords:
            if keyword.lower() not in meta_keywords:
                keyword_matched = False
                break

        if keyword_matched:
            filtered_products.append(product.meta_keyword)

    if not filtered_products:
      
        individual_keywords_query = Q()
        for keyword in keywords:
            individual_keywords_query |= Q(meta_keyword__icontains=keyword)

        filtered_products = Product.objects.filter(status=0).filter(individual_keywords_query).values_list('product_name','meta_keyword', flat=True).distinct()

    product_list = list(set(filtered_products))
    return JsonResponse(product_list, safe=False)  

 

def load_more_data(request):
    offset=int(request.GET['offset'])
    limit=int(request.GET['limit'])
    data=Product.objects.all().order_by('-uid')[offset:offset+limit]
    t=render_to_string('ajax/product_list.html',{'data':data})
    return JsonResponse({'data':t}
)
def search_results(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(status=0, meta_keyword__icontains=query)
    total_data=Product.objects.count()
    all_gender=gender.objects.all()
    all_catdisp=Category.objects.all()
    all_color=ColorVariant.objects.all()
    all_size=SizeVariant.objects.all()
   # images=ProductAttribute.objects.all().values('image')
    
    minMaxprice=ProductAttribute.objects.aggregate(Min('selling_price'),Max('selling_price'))
    print(minMaxprice)
   
    context = {
        'products': products,
        'query': query,
        'all_gender':all_gender,
                'all_catdisp':all_catdisp,
                'all_color':all_color,
                'all_size':all_size ,
                'total_data':total_data,
                'minMaxprice':minMaxprice
    }
    return render(request,'account/product_list.html',context)

def get_image(request):
    if request.method == 'POST' and ('HTTP_X_REQUESTED_WITH' in request.META and request.META['HTTP_X_REQUESTED_WITH'] == 'XMLHttpRequest'):
      
        color = request.POST.get('color')
        print("the color is ",color)
        product_attribute_id = request.POST.get('product_attribute_id')
        print("attribute is",product_attribute_id )

     
        try:
            product_attribute = get_object_or_404(ProductAttribute, uid=product_attribute_id, colorVariant__uid=color)
            print("the atrr",product_attribute)
            product_image = product_attribute.product_images.first()
            print("the image",product_image)
            image_url = product_image.image.url if product_image else ''
            print("the image url",image_url)
        except ProductAttribute.DoesNotExist:
            image_url = ''

        
        return JsonResponse({'image': image_url})

    
    return JsonResponse({})