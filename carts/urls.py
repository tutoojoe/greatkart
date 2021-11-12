from django.urls import path
from . import views



urlpatterns = [
    path('',views.cart, name='cart'),
    
    path('add_cart/<int:product_id>/',views.add_cart,name='add_cart'),
    path('add_cart_ajax/',views.add_cart_ajax,name='add_cart_ajax'),
    path('add_wishlist/',views.add_wishlist,name='add_wishlist'),
    path('wishlist/',views.wishlist,name='wishlist'),
    path('remove_wish_item/',views.remove_wish_item, name='remove_wish_item'),
    

    path('remove_cart/<int:product_id>/<int:cart_item_id>/',views.remove_cart, name='remove_cart'),
    path('remove_cart_ajax/',views.remove_cart_ajax, name='remove_cart_ajax'),
    path('remove_cart_item/',views.remove_cart_item, name='remove_cart_item'),

     path('checkout/',views.checkout, name="checkout"),

]

