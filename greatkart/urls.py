"""greatkart URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('django_admin/', admin.site.urls),
    path('', views.home, name = 'home'),
    # path('add_product/',views.add_product,name='add_product'),
    
    path('store/',include('store.urls')),
    path('cart/',include('carts.urls')),
    path('accounts/',include('accounts.urls')),
    # orders
    path('orders/',include('orders.urls')),
    path('admin/',include('mycartadmin.urls')),
    path('coupon_offers/',include('coupon_offers.urls')),
    
    
]

admin.site.index_title = "GreatKart"
admin.site.site_header = "GreatKart Admin"
admin.site.site_title = "Admin"

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)