from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [

    path('coupon_apply/',views.coupon_apply,name='coupon_apply'),
    path('verify_coupon/',views.verify_coupon,name='verify_coupon'),

]