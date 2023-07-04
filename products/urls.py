from django.contrib import admin
from django.urls import path,include
from .import views


urlpatterns = [
    path('',views.indexpage,name='indexpage'),
    path('gender_view/<str:uid>',views.gender_view,name='gender_view'),
    path('category_view/ <str:uid>',views.category_view,name='category_view'),
    path('product_list',views.product_list,name='product_list'),
    path('all_products',views.all_products,name='all_products'),
    path('filter_data',views.filter_data,name='filter_data'),
    path('product_detail/ <str:uid>',views.product_detail,name='product_detail'),
    path('category_view/product_detail/<str:uid>',views.product_detail,name='product_detail'),
    path('gender_view/product_detail/<str:uid>',views.product_detail,name='product_detail'),
   # path('accounts/gender_view/nextimage/<str:uid>',views.nextimage,name='nextimage'),
    path('search',views.search,name='search'),
   
    path('load-more-data',views.load_more_data,name='load-more-data'),
    path('search/results', views.search_results, name='search_results'),
    path('get-image/', views.get_image, name='get_image'),
  



]


