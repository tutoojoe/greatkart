from django.urls import path
from . import views

urlpatterns = [
    path('',views.admin_page_view,name='admin_page_view'),
    path('admin_login',views.admin_login, name='admin_login'),
    path('admin_logout',views.admin_logout, name = 'admin_logout'),
    path('admin_dashboard',views.admin_dashboard, name='admin_dashboard'),

    # banner
    path('admin_banners',views.admin_banners, name='admin_banners'),    
    path('add_banner',views.add_banner, name='add_banner'),

    # orders & sales report filters
    path('admin_orders',views.admin_orders, name = 'admin_orders'),
    path('sales_report',views.sales_report, name = 'sales_report'),
    
    path('order_report',views.order_report, name='order_report'),
    path('filter_orders',views.filter_orders, name='filter_orders'),
    path('update_order_status/<int:order_no>',views.update_order_status, name='update_order_status'),


    # category
    path('admin_category',views.admin_category, name = 'admin_category'),
    path('add_category',views.add_category, name = 'add_category'),
    path('edit_category/<int:id>',views.edit_category, name = 'edit_category'),
    path('delete_category/<int:id>',views.delete_category, name = 'delete_category'),
    
    
    
    # manage users
    path('usermanage',views.usermanage, name = 'usermanage'),
    path('admin_user_deactivate/',views.admin_user_deactivate, name = 'admin_user_deactivate'),
    path('admin_user_activate/',views.admin_user_activate, name = 'admin_user_activate'),
    path('admin_user_edit/<int:id>',views.admin_user_edit, name = 'admin_user_edit'),
    path('admin_user_delete/',views.admin_user_delete, name = 'admin_user_delete'),


    # product 
    path('admin_product',views.admin_product, name = 'admin_product'),
    path('add_product',views.add_product, name = 'add_product'),
    path('edit_product/<int:id>',views.edit_product, name = 'edit_product'),
    path('admin_prod_delete/<int:id>',views.admin_prod_delete, name = 'admin_prod_delete'),
    path('add_gallery_images/',views.add_gallery_images, name = 'add_gallery_images'),
    path('add_prod_variation/',views.add_prod_variation, name = 'add_prod_variation'),
    path('edit_gallery_images/<int:id>',views.edit_gallery_images, name = 'edit_gallery_images'),
    path('view_product_images/',views.view_product_images, name = 'view_product_images'),
    path('del_gal_image/<int:id>',views.del_gal_image, name = 'del_gal_image'),
    

    
    #offers
    path('admin_offers',views.admin_offers, name = 'admin_offers'),
    path('add_coupon',views.add_coupon, name = 'add_coupon'),
    path('edit_coupon/<int:c_id>',views.edit_coupon, name = 'edit_coupon'),    
    path('activate_coupon',views.activate_coupon, name = 'activate_coupon'),     
    path('block_coupon',views.block_coupon, name = 'block_coupon'),
    path('delete_coupon',views.delete_coupon, name = 'delete_coupon'),

    path('add_product_offer',views.add_product_offer, name = 'add_product_offer'),
    path('edit_product_offer/<int:prod_id>',views.edit_product_offer, name = 'edit_product_offer'),    
    path('activate_product_offer',views.activate_product_offer, name = 'activate_product_offer'),     
    path('block_product_offer',views.block_product_offer, name = 'block_product_offer'),
    path('delete_product_offer',views.delete_product_offer, name = 'delete_product_offer'),

    path('add_cat_offer',views.add_cat_offer, name = 'add_cat_offer'),
    path('edit_cat_offer/<int:cat_id>',views.edit_cat_offer, name="edit_cat_offer"),
    path('activate_cat_offer',views.activate_cat_offer, name = 'activate_cat_offer'),     
    path('block_cat_offer',views.block_cat_offer, name = 'block_cat_offer'),
    path('delete_cat_offer',views.delete_cat_offer, name = 'delete_cat_offer'),


]