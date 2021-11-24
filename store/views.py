
from django.core import paginator
from django.core.checks import messages
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from carts import context_processors
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id
from orders.models import OrderProduct
from store.forms import Reviewforms
from store.models import Product, ProductGallery, ReviewRating
from django.core.paginator import EmptyPage, Page, PageNotAnInteger, Paginator
from django.db.models import Q
from django.contrib import messages
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required




# Create your views here.

def store(request,category_slug=None,):

    categories      = None
    products        = None
    if category_slug != None:
        categories      = get_object_or_404(Category,slug=category_slug)
        products        = Product.objects.filter(category = categories,is_available = True)
        paginator       = Paginator(products, 6)
        page            = request.GET.get('page')
        paged_products  = paginator.get_page(page)
        product_count   = products.count()
        
    else:
        products        = Product.objects.all().filter(is_available=True).order_by('id')
        paginator       = Paginator(products, 6)
        page            = request.GET.get('page')
        paged_products  = paginator.get_page(page)
        product_count   = products.count()
        

    context     = {
        'products' : paged_products,
        'product_count': product_count,
        }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
   
    try:

        single_product  = Product.objects.get(category__slug = category_slug, slug = product_slug,)
        in_cart         = CartItem.objects.filter(cart__cart_id = _cart_id(request), product = single_product).exists()
     

    except Exception as e:
        raise e

    try:
        orderproduct = OrderProduct.objects.filter(user = request.user, product_id = single_product.id).exists()
    
    except:
        orderproduct = None

    reviews = ReviewRating.objects.filter(product_id = single_product.id, status = True)
    produt_gallery = ProductGallery.objects.filter(product_id = single_product.id)

    context = {
        'orderproduct'          : orderproduct,
        'single_product'        : single_product,
        'in_cart'               : in_cart,
        'reviews'               : reviews,
        'product_gallery'       :produt_gallery
    }

    return render(request,'store/product_detail.html',context)


def search(request):
    
    if 'keyword' in request.GET:
        keyword     = request.GET['keyword']
        if keyword:
            products    = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) |Q(product_name__icontains=keyword)| Q(slug__contains=keyword))
            # '__icontains' will search for the matching keyword anywhere in the "description" and return 
            # the result OR - anywhere in product name. We have to add 'Q'
            product_count   = products.count()
        else:
            return redirect ('store')

    context     = {
        'products':products,
        'product_count':product_count,
        }
    return render(request,'store/store.html', context)


login_required(login_url='login')
def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        try:
            reviews = ReviewRating.objects.get(user__id = request.user.id, product__id = product_id)
            form = Reviewforms(request.POST, instance= reviews)
            form.save()
            messages.success(request,"Thanks!. Your review has been successfully updated.")
            return redirect(url)        

        except ReviewRating.DoesNotExist:
            form = Reviewforms(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request,"Thanks!. Your review has been submitted.")
                return redirect(url) 


