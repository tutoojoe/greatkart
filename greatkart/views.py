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
            
            print(p_offer.discount,'for',product)
        except:
            pass
        
        try:
            categ_offer = CategoryOffer.objects.get(category_id = product.category,valid_from__lte=now, valid_to__gte=now, is_active = True)
            c_offer = categ_offer.discount
            print(c_offer.discount,'for',product,'- is the product and ',product.category)
        except:
            pass

        if p_offer > c_offer:
            disc_price = product.mrp_price - (product.mrp_price * p_offer)/100
            product.price = round(disc_price, 2)
            product.save()
            print(disc_price, 'product - ',product, ' this will be the new price based on product offer. Old price was - ',product.mrp_price)
            # print(product,' - ', p_offer.discount,'product offer is more')
        elif p_offer < c_offer:
            disc_price = product.mrp_price - (product.mrp_price * c_offer)/100
            product.price = disc_price
            product.save()
            print(disc_price, 'product - ',product,' this will be the new price based on CATEGORY. Old price was - ',product.mrp_price)
            # print(c_offer.discount,' - ', 'category offer is more')
        elif p_offer == c_offer and p_offer !=0 :
            print('here both the offers are same for this product', product)
            disc_price = product.mrp_price - (product.mrp_price * p_offer)/100
            product.price = disc_price
            product.save()

        else:
            print(product, ' - this one has no offer')
        
    reviews = ReviewRating.objects.filter(product_id = prod_id, status = True)

    context     = {
        'products': products,
        'reviews' : reviews,
        'banners': banners,
    }

    return render(request, 'home.html',context)

def images(request):
    print('request received')
    if request.method == "POST":
        form = ProductForm(request.POST or None, request.FILES or None)

        if form.is_valid():
            print('Form Valid')
            print('form valid')
            product_name = form.cleaned_data['product_name']
            slug = slugify(product_name)
            print(slug)
            description = form.cleaned_data['description']
            price = form.cleaned_data['price']
            
            images = form.cleaned_data['images']
            stock = form.cleaned_data['stock']
            is_available = form.cleaned_data['is_available']
            category = form.cleaned_data['category']
            
            product = Product.objects.create(product_name=product_name, slug=slug, description=description,mrp_price=price,price=price,images=images,stock=stock,is_available=is_available,category=category)
            product.save()
            
            return redirect('images')
    else:
        print('Form Valid')
        form = ProductForm()
    context     = {
            'form' : form,
        }
    return render(request,'image.html',context)


# def add_product(request):
#     form = ProductForm(request.POST or None, request.FILES or None)
#     if form.is_valid():
#         form.save()
        
#         return JsonResponse({'message':'works'})
#     context     = {
#             'form' : form,
#         }
#     return render(request,'image.html',context)