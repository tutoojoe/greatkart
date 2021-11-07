from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.register, name='register'),
    path('add_address/',views.add_address, name='add_address'),
    path('login/',views.login, name='login'),
    path('logout/',views.logout, name='logout'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('',views.dashboard, name='dashboard'),
    path('verify_otp/',views.verify_otp, name='verify_otp'),


    path('activate/<uidb64>/<token>',views.activate, name='activate'),
    path('my_orders/',views.my_orders,name='my_orders'),
    path('my_addresses/',views.my_addresses,name='my_addresses'),
    path('edit_profile/',views.edit_profile,name='edit_profile'),
    path('change_password/',views.change_password,name='change_password'),
    path('order_detail/<order_id>/',views.order_detail,name='order_detail'),
    path('delete_address/<int:add_id>/',views.delete_address,name='delete_address'),


]

