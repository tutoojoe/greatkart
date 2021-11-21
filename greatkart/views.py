from typing import ContextManager
from django.http.response import JsonResponse
from django.urls import path
from django.shortcuts import render,redirect
from coupon_offers.models import CategoryOffer, ProductOffer
from mycartadmin.models import BannerUpdate
from store.forms import ProductForm
from store.models import Product,ReviewRating
from datetime import timezone
from datetime import datetime
from django.utils.text import slugify



def home(request):
    now = datetime.now()
    
    # prod_offers = ProductOffer.objects.filter(valid_from__lte=now, valid_to__gte=now, is_active = True)
    # categ_offers = CategoryOffer.objects.filter(valid_from__lte=now, valid_to__gte=now, is_active = True)
    # for c_offer in categ_offers:
    #     print(c_offer,'cat - offer')
    #     print(c_offer.category_id, 'category')
    #     print(c_offer.category_id.id, 'category id')
    #     print(c_offer.discount, 'category discount')

    # for p_offer in prod_offers:
    #     print(p_offer,' pro offer')
    #     print(p_offer.product_id, 'prod name')
    #     print(p_offer.product_id.id, 'prod id')
    #     print(p_offer.discount, 'prod discount')

    banners = BannerUpdate.objects.filter(valid_from__lte=now, valid_to__gte=now, is_active = True)

    products    = Product.objects.all().filter(is_available=True).order_by('created_date')
    
    for product in products:
        p_offer = 0
        c_offer = 0
        prod_id = product.id
        try:
            prod_offer = ProductOffer.objects.get(product_id = product, valid_from__lte=now, valid_to__gte=now, is_active = True)
            p_offer = prod_offer.discount
            
            
        except:
            pass
        
        try:
            categ_offer = CategoryOffer.objects.get(category_id = product.category,valid_from__lte=now, valid_to__gte=now, is_active = True)
            c_offer = categ_offer.discount
            
        except:
            pass

        if p_offer > c_offer:
            disc_price = product.mrp_price - (product.mrp_price * p_offer)/100
            product.price = round(disc_price, 2)
            product.discount_percentage = p_offer
            product.save()
        elif p_offer < c_offer:
            disc_price = product.mrp_price - (product.mrp_price * c_offer)/100
            product.price = round(disc_price,2)
            product.discount_percentage = c_offer
            product.save()
            
        elif p_offer == c_offer and p_offer !=0 :
       
            disc_price = product.mrp_price - (product.mrp_price * p_offer)/100
            product.discount_percentage = p_offer
            product.price = round(disc_price,2)
            product.save()

        elif p_offer == c_offer == 0:
            product.price = product.mrp_price
            product.save()
        
        
    reviews = ReviewRating.objects.filter(product_id = prod_id, status = True)

    context     = {
        'products': products,
        'reviews' : reviews,
        'banners': banners,
    }

    return render(request, 'home.html',context)



# def add_product(request):
#     form = ProductForm(request.POST or None, request.FILES or None)
#     if form.is_valid():
#         form.save()
        
#         return JsonResponse({'message':'works'})
#     context     = {
#             'form' : form,
#         }
#     return render(request,'image.html',context)