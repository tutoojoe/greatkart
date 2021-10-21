from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.register, name='register'),
    path('login/',views.login, name='login'),
    path('logout/',views.logout, name='logout'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('',views.dashboard, name='dashboard'),
    path('verify_otp/',views.verify_otp, name='verify_otp'),


    path('activate/<uidb64>/<token>',views.activate, name='activate'),




   


]

