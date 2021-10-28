from typing import ContextManager
from django.urls import path
from django.shortcuts import render
from store.models import Product,ReviewRating


def home(request):
    products    = Product.objects.all().filter(is_available=True).order_by('created_date')
    for product in products:
        product_id = product.id
    reviews = ReviewRating.objects.filter(product_id = product_id, status = True)
    context     = {
        'products':products,
        'reviews' : reviews,
    }

    return render(request, 'home.html',context)