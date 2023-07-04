from django.shortcuts import render,redirect,reverse
from django.http import JsonResponse
from accounts.models import User
from products.models import *
from .models import *
from django.contrib import messages
from userprofile.models import *
from django.db.models import Q
from cartify.models import *
import random
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.http import HttpResponse
from userprofile.models import *
import string
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph,Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
import requests


def generate_referral_code():
    characters = string.ascii_letters + string.digits
    referral_code = ''.join(random.choices(characters, k=8))
    return referral_code
def generate_tracking_number():
    return 'Skittish' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


def placeorder(request):
    if request.method == 'POST':
        user_wallet = Wallet.objects.get(user=request.user)
        neworder = Order()
        neworder.user = request.user
        address_uids = request.POST.get('addresses').split(',')
        addresses = [get_object_or_404(Address, uid=uid) for uid in address_uids]
        neworder.address = addresses[0]
        neworder.payment_mode = request.POST.get('payment_mode')
        neworder.payment_id = request.POST.get('payment_id')
        coupon = Cart.get_coupon(request.user)
        grand_total = Cart.calculate_grand_total(request.user)
        
        neworder.total_price = grand_total
        track_num = generate_tracking_number()
        while Order.objects.filter(tracking_number=track_num).exists():
            track_num = generate_tracking_number()
        neworder.tracking_number = track_num
        neworder.save()

        neworderitems = Cart.objects.filter(user=request.user)
        for item in neworderitems:
            orderitem.objects.create(
                order=neworder,
                product=item.product,
                product_price=item.total_price,
                size=item.size,
                color=item.color,
                product_qty=item.product_qty,
                productattr=item.productattr,
                total_price=grand_total,
            )
            orderproduct = ProductAttribute.objects.filter(uid=item.productattr_id).first()
            orderproduct.quantity = orderproduct.quantity - item.product_qty
            orderproduct.save()

            # Set the discount to 0 for the cart item
            user_wallet.discount = 0
            user_wallet.save()
            item.save()
        


        if neworder.payment_mode == 'Wallet':
            if user_wallet.amount >= neworder.total_price:
                user_wallet.amount -= neworder.total_price
                user_wallet.save()
            else:
                return render(request, 'order/order.html', {'status': 'Insufficient wallet balance'})

        referring_user = request.user
        if referring_user.referral_code is None and orderitem.objects.filter(order__user=referring_user).count() > 5:
            referral_code =  generate_referral_code()
            referring_user.referral_code =  referral_code
            print("the referral code is", referral_code)
            referring_user.save()
        Cart.objects.filter(user=request.user).delete()
        
        return JsonResponse({'status':"Order placed successfully"})
    else:
        return render(request, 'order/order.html')


        
def proceed_to_pay(request):
    print("i am in proceed")
    cart=Cart.objects.filter(user=request.user)
    grand_total = Cart.calculate_grand_total(request.user)
    return JsonResponse({'grand_total':grand_total})

def my_orders(request):
    order=Order.objects.filter(user=request.user).order_by('-id')
    print(order)
    context={'order':order}
    return render(request,'order/order_list.html',context)
def my_order_items(request, id):
    oderit = orderitem.objects.filter(order_id=id) 
    delivered_date = None
    time_difference = None
    print(oderit)
    grand_total = Cart.calculate_grand_total(request.user)
    
    for item in oderit:
        item.progress_percentage = item.calculate_progress_percentage()
        if item.delivered_date is not None:
            item.time_difference = timezone.now().date() - item.delivered_date
            print("time_difference", item.delivered_date)
        print(item.progress_percentage)

    
    context = {'oderit': oderit, 'grand_total': grand_total, 'time_difference': time_difference}
    return render(request, 'order/order.html', context)




def order_cancel(request, id):
    order = get_object_or_404(orderitem, id=id)
    
    if order.status == 'Pending':
        order.status = 'Cancelled'
        order.save()
        
       
        return render(request, 'order/order.html', {'message': 'success'})
    else:
        
        return render(request, 'order/order.html', {'message': 'warning'})
    
   
    
    
def return_product(request,id):
     item=orderitem.objects.get(id=id)
     context={'item':item}
     return render(request,'order/return_form.html',context)
 
def process_return(request, id):
    print(id)
    order_item = orderitem.objects.get(id=id)
    order = order_item.order
    

    if request.method == 'POST':
        reason = request.POST.get('reason')
        print(reason)
        order_item.return_reason = reason
        if order_item.status == 'Successfully Delivered':

            order_item.status = 'return'
            order_item.save()
        
            return render(request, 'account/returnplaced.html', {'message': 'success'})
    
 
    return render(request, 'account/returnplaced.html', {'message': 'warning'})


def rewiew_rating(request, id):
     item=orderitem.objects.filter(product_id=id).first()
     context={'item':item}
     return render(request,'order/review.html',context)
 
def reviews(request,uid):
    if request.method == 'POST':
        reason = request.POST.get('reason')
        rating = int(request.POST.get('rating'))
        print(uid)
        
        Review.objects.create(
            comment=reason,
            user=request.user,
            product_id=uid,
            rating=rating
        )
        
      
        return render(request, 'account/reviewplaced.html', {'message': 'success'})
    
    
    return redirect('/oders/my_orders')

def download_invoice(request, id):
    item = orderitem.objects.get(order_id=id)

    # Create the PDF file
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=letter)

    # Build the PDF content
    elements = []

    # Add the Flipkart logo and heading
    flipkart_logo_url = "https://res.cloudinary.com/zenbusiness/q_auto/v1/logaster/logaster-2019-02-0008-t-shoe-splash-logo.png"
    response = requests.get(flipkart_logo_url)
    if response.status_code == 200:
        logo_image = Image(BytesIO(response.content), width=150, height=50)
        elements.append(logo_image)
    else:
        elements.append(Paragraph("Flipkart Logo", styles['Heading1']))
    elements.append(Spacer(1, 20))

    # Get the styles
    styles = getSampleStyleSheet()

    # Add the heading
    heading = Paragraph('<b>Tax Invoice</b>', styles['Heading1'])
    elements.append(heading)
    elements.append(Spacer(1, 20))

    # Add the delivery date
    delivery_date = f"<b>Delivery Date:</b> {item.delivered_date}"
    delivery_date_paragraph = Paragraph(delivery_date, styles['BodyText'])
    elements.append(delivery_date_paragraph)
    elements.append(Spacer(1, 20))
    
    
    ship_from_table_data = [
        [''],
        [Paragraph('<u><b>Ship From:</b></u>', styles['BodyText'])],
        ['Skittish shop'],
        ['123 Street Name'],
        ['City, State, Country'],
        ['Postal Code'],
    ]

    ship_from_table_style = TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
    ])

    ship_from_table = Table(ship_from_table_data, style=ship_from_table_style)
    elements.append(ship_from_table)

    # Create the data table
    table_data = [
        [ 'Product', 'Size', 'Color', 'Quantity', 'Product Price', 'Grand Total'],
        [ str(item.product.product_name), str(item.size), str(item.color),
         str(item.product_qty), str(item.product_price), str(item.total_price)],
    ]

    # Create the table and apply the style
    table_style = TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Header row text color
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),  # Header row background color
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header row font style
        ('FONTSIZE', (0, 0), (-1, 0), 14),  # Header row font size
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Header row bottom padding
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  # Grid lines
    ])
    table = Table(table_data, style=table_style)
    elements.append(table)

    # Create the address table
    address_table_data = [
        [''],
        [
            Paragraph('<u><b>Shipping To:</b></u>', styles['BodyText']),
            Paragraph('<u><b>Billing To:</b></u>', styles['BodyText'])
        ],
        [
            f"{item.order.address.username}",
            f" {item.order.address.username}"
        ],
        [
            f"{item.order.address.address}",
            f" {item.order.address.address}"
        ],
        [
            f" {item.order.address.city}",
            f" {item.order.address.city}"
        ],
        [
            f" {item.order.address.state}",
            f" {item.order.address.state}"
        ],
        [
            f" {item.order.address.country}",
            f"{item.order.address.country}"
        ],
        [
            f" {item.order.address.pincode}",
            f" {item.order.address.pincode}"
        ],
    ]
    address_table_style = TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
    ])
    address_table = Table(address_table_data, style=address_table_style)
    elements.append(address_table)

    # Build the PDF
    pdf.build(elements)

    # Get the PDF file from the buffer
    buffer.seek(0)

    # Create the HTTP response with the PDF file
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=invoice_{item.id}.pdf'

    return response