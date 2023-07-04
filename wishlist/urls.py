from django.contrib import admin
from django.urls import path,include
from .import views


urlpatterns = [
    path('wishlist', views.wishlist,name='wishlist'),
    path('add_wishlist', views.add_wishlist,name='add_wishlist'),
    path('delete_wishlist', views.delete_wishlist,name='delete_wishlist'),
    path('wishlistempty', views.wishlistempty,name='wishlistempty'),

]
