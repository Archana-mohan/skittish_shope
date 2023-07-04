
from django.urls import path,include
from .import views

urlpatterns = [ 
    path('placeorder', views.placeorder,name='placeorder'),
    path('proceed_to_pay', views.proceed_to_pay,name='proceed_to_pay'),
    path('my_orders', views.my_orders,name='my_orders'),
    path('my_order_items/<str:id>', views.my_order_items,name='my_order_items'),
    path('order_cancel/<str:id>', views.order_cancel,name='order_cancel'),
    path('return_product/<str:id>', views.return_product,name='return_product'),
    path('process_return/<str:id>', views.process_return,name='process_return'),
    path('rewiew_rating/<str:id>', views.rewiew_rating,name='rewiew_rating'),
    path('reviews/<str:uid>', views.reviews,name='reviews'),
    path('download_invoice/<str:id>', views.download_invoice,name='download_invoice'),
    
]

