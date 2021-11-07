from django.urls import path
from . import views

urlpatterns = [
    path('',views.admin_page_view,name='admin_page_view'),
    path('admin_login',views.admin_login, name='admin_login'),
    path('order_report',views.order_report, name='order_report'),
    path('filter_orders',views.filter_orders, name='filter_orders'),   
    path('admin_dashboard',views.admin_dashboard, name='admin_dashboard'),
    path('admin_logout',views.admin_logout, name = 'admin_logout'),
    path('usermanage',views.usermanage, name = 'usermanage'),
    path('admin_category',views.admin_category, name = 'admin_category'),
    path('admin_product',views.admin_product, name = 'admin_product'),
    path('add_product',views.add_product, name = 'add_product'),
    path('edit_product/<int:id>',views.edit_product, name = 'edit_product'),
    path('add_category',views.add_category, name = 'add_category'),
    path('edit_category/<int:id>',views.edit_category, name = 'edit_category'),
    path('admin_orders',views.admin_orders, name = 'admin_orders'),
    path('admin_offers',views.admin_offers, name = 'admin_offers'),
    path('admin_user_deactivate/',views.admin_user_deactivate, name = 'admin_user_deactivate'),
    path('admin_user_activate/',views.admin_user_activate, name = 'admin_user_activate'),
    path('admin_user_edit/<int:id>',views.admin_user_edit, name = 'admin_user_edit'),
    path('admin_user_delete/',views.admin_user_delete, name = 'admin_user_delete'),
    path('update_order_status/<int:order_no>',views.update_order_status, name='update_order_status'),

]