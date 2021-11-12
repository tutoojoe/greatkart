from django.urls import path
from . import views

urlpatterns = [
    path('place_order/',views.place_order,name='place_order'),
    path('payments/',views.payments,name='payments'),
    path('order_complete/',views.order_complete, name='order_complete'),
    path('rzp_order_complete/',views.rzp_order_complete, name='rzp_order_complete'),
    path('cod_order_complete/<int:order_number>',views.cod_order_complete, name='cod_order_complete'),
    path('proceed_payment/',views.proceed_payment,name='proceed_payment'),
    path('user_order_cancel/<int:order>',views.user_order_cancel, name='user_order_cancel'),
    path('user_order_return/<int:order>',views.user_order_return, name='user_order_return'),
    
    

    
]