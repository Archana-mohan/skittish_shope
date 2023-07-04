from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from .import views

urlpatterns = [
    path('',views.adminlogin,name='adminlogin'),
    path('adminlogout',views.adminlogout,name='adminlogout'),
    path('adforgottern',views.adforgottern,name='adforgottern'),
    path('addproducts',views.addproducts,name='addproducts'),
    path('mainpage',views.mainpage,name='mainpage'),
    path('userdetails',views.userdetails,name='userdetails'),
    path('adduser',views.adduser,name='adduser'),
    path('edit',views.edit,name='edit'),
    path('update/ <str:id>',views.update,name='update'),
    path('delete/<str:id>',views.delete,name='delete'),
#   path('block/<str:id>',views.block,name='block'),
    path('product_details',views.product_details,name='product_details'),
    path('product_update/<str:uid>',views.product_update ,name='product_update'),
    path('product_delete/<str:uid>',views.product_delete,name='product_delete'),
    path('adding_product',views.adding_product ,name='adding_product'),
    path('product_variations/<str:uid>',views.product_variations,name='product_variations'),
    path('add_image/<str:uid>',views.add_image,name='add_image'),
    path('category_update /<str:uid>', views.category_update,name='category_update'),
    path('category_delete /<str:uid>', views.category_delete,name='category_delete'),
    path('add_category', views.add_category,name='add_category'),
    path('Category_details', views.Category_details,name='Category_details'),
    path('add_coupon', views.add_coupon,name='add_coupon'),
    path('edit_coupon/<str:id>', views.edit_coupon,name='edit_coupon'),
    path('delete_coupon/<str:id>', views.delete_coupon,name='delete_coupon'),
    path('new_coupon', views.new_coupon,name='new_coupon'),
    path('monthgraphical',views.monthgraphical,name='monthgraphical'),
    path('yeargraphical',views.yeargraphical,name='yeargraphical'),
    path('weekgraphical',views.weekgraphical,name='weekgraphical'),
    path('order_list',views.order_list,name='order_list'),
    path('order_list2',views.order_list2,name='order_list2'),
    path('order_cancelled/<str:id>',views.order_cancelled,name='order_cancelled'),
    path('order_update/<str:id>',views.order_update,name='order_update'),
    path('admin_profile',views.admin_profile,name='admin_profile'),
    path('admin_bank',views.admin_bank,name='admin_bank'),
    path('security_settings',views.security_settings,name='security_settings'),
    path('salesreport',views.salesreport,name='salesreport'),
    path('delete_account/<str:id>',views.delete_account,name='delete_account'),
    path('edit_account/<str:id>',views.edit_account,name='edit_account'),
    path('productvar_delete/<str:uid>',views.productvar_delete,name='productvar_delete'),
    path('orderdetail/<str:id>',views.orderdetail,name='orderdetail'),
    path('approve_return/<str:id>',views.approve_return,name='approve_return'),
    
] 
