
from django.urls import path,include
from .import views

urlpatterns = [ 
    path('address', views.address,name='address'),
    path('addaddress', views.addaddress,name='addaddress'),
    path('address_delete <str:uid>',views.address_delete,name='address_delete'),
    path('edit_address <str:uid>',views.edit_address,name='edit_address'),
    path('user_profile',views.user_profile,name='user_profile'),
    path('user_address',views.user_address,name='user_address'),
    path('settings',views.settings,name='settings'),
    
]
