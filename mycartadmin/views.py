from datetime import date
from django import contrib
from django.contrib.auth import authenticate,login,logout
from django.contrib.messages.api import success
from django.forms import forms
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls.conf import path
from django.views.decorators.cache import cache_control
from category.models import Category
from coupon_offers.forms import CategoryOfferForm, CouponApplyForm, ProductOfferForm
from mycartadmin.forms import BannerUpdateForm
from mycartadmin.models import BannerUpdate
from orders.forms import OrderForm, OrderStatusForm
from store.forms import ProductForm, ProductGalleryForms
from category.forms import CategoryForm
from store.models import Product
from orders.models import Order, OrderProduct, Payment
from accounts.models import Account
from coupon_offers.models import Coupon,ProductOffer,CategoryOffer
import mycartadmin
from django.core.paginator import Paginator
from django.utils.text import slugify
from django.db.models import Avg, Count, Min, Max, Sum,FloatField
from datetime import datetime
from django.db.models import Count, DateTimeField
from django.db.models.functions import Trunc

from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors



def filter_orders(request):
    data = []
    data.append(['Name','Order Number','Phone No','Order Value'])
 
    if request.method == "POST":
        
        from_date = request.POST["from_date"]
        to_date = request.POST["to_date"]
        orders = Order.objects.filter(created_at__range=(from_date, to_date))

        # for order in orders:
        #     data.append([str(order.first_name),str(order.order_number),str(order.phone),str(order.order_total)])

        # print(data)

        # fileName = 'orders.pdf'

        # pdf = SimpleDocTemplate(
        #     fileName,
        #     pagesize = letter,
        # )

        # table = Table(data)
        # print('going to print the data')
        # style = TableStyle([
        #     ('BACKGROUND',(0,0),(4,0),colors.green),
        #     ('TESTCOLOR',(0,0),(-1,0),colors.whitesmoke),
        #     # ('ALIGN',(0,0),(-1,-1),'CENTER'),
        #     # ('ALIGN',(1,0),(-1,-1),'CENTER'),
        #     ('FONTNAME',(0,0),(-1,0),'Courier-Bold'),
        #     ('FONTSIZE',(0,0),(-1,0),14),
            
        #     ('BOTTOMPADDING',(0,0),(-1,0),12),
        #     ('BACKGROUND',(0,1),(-1,-1),colors.beige),
        # ])
        # table.setStyle(style)


        # elems = []
        # elems.append(table)
        # pdf.build(elems)

    context = {
        'orders': orders,
    }

    return render(request, 'mycartadmin/orders.html', context)
    
    


def order_report(request):
    #create bytestream buffer
    buf = io.BytesIO()
    # create a canvas
    c = canvas.Canvas(buf,pagesize=letter, bottomup=0)
    #create a text opject for canvas 
    c.setTitle("GreatKart")
    c.setSubject("Orders - Filtered within the give range")

    textobj = c.beginText()
    textobj.setTextOrigin(inch,inch)
    textobj.setFont("Helvetica",12)
    lines = []
    if request.method == "POST":
        
        from_date = request.POST["from_date"]
        to_date = request.POST["to_date"]
        orders = Order.objects.filter(created_at__range=(from_date, to_date))

    for order in orders:
        lines.append([str(order.first_name),str(order.order_number),str(order.phone),str(order.order_total)])


  
    # filename = 'orders.pdf'






    # from here the old items start
    for line in lines:
        textobj.textLine(str(line))


    c.drawText(textobj)
    c.showPage()
    c.save()
    buf.seek(0)


    return FileResponse(buf, as_attachment=True,filename='filtered_orders.pdf')


def admin_banners(request):
    banners = BannerUpdate.objects.all()
    context = {
        'banners': banners,
    }

    return render(request, 'mycartadmin/admin_banners.html',context)


# Create your views here.
def admin_login(request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
            
                return redirect('admin_dashboard')
            else:
                messages.error(request, "You dont have admin privileges to view this page.")
                return redirect('home')
        else:
        
            return render(request,'mycartadmin/login.html')

@login_required(login_url='admin_login')
def admin_dashboard(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            
            total_ord_no = Order.objects.all().count()
            total_user_no = Account.objects.all().count()         
            
            total_order_value = Order.objects.all().aggregate(Sum('order_total'))
            # print(total_order_value['order_total__sum'],'total order value')

            avg_ord_value = Order.objects.all().aggregate(average_order_value = Avg('order_total'))
            
            val_diff = Order.objects.aggregate(value_diff = Max('order_total', output_field = FloatField())-Avg('order_total'))
                       
            orders_per_day = Order.objects.annotate(order_day=Trunc('created_at', 'day', output_field=DateTimeField())).values('order_day').annotate(orders=Count('id')).order_by('-order_day')[:7]
            ord_val_per_day = Order.objects.annotate(order_day=Trunc('created_at', 'day', output_field=DateTimeField())).values('order_total').annotate(ord_value=Sum('id')).order_by('-order_day')[:7]
            # qty_product = Order.objects.annotate(num_prod=Count('product'))
            # print(qty_product)
            latest_order = Order.objects.all().order_by('-created_at')[:5]
          
            # sample = OrderProduct.objects.annotate(Sum('quantity'))

            # print(sample)    

            
        
                        
            labels = []
            ord_data = []
            val_data = []
            category = []
            cat_prod_qty = []
            
            pay_method = Order.objects.annotate(pay_method=Count('payment'))
            
            
            prod_in_cat = Category.objects.annotate(prod_count=Count('product'))
            for i in prod_in_cat:
                category.append(i.category_name)
                cat_prod_qty.append(i.prod_count)
        
            


            for ord in orders_per_day:
                # print(ord['order_day'], ord['orders'])
                labels.append(str(ord['order_day'].date()))
                ord_data.append(ord['orders'])

            for val in ord_val_per_day:
                val_data.append(int(val['ord_value']))
            
        
            labels.reverse()
            # val_data.reverse()
            ord_data.reverse()
           

            context = {
                'latest_order':latest_order,
                'category':category,
                'cat_prod_qty':cat_prod_qty,
                'labels':labels,
                'data':ord_data,
                'val_data':val_data,
                'total_user_no':total_user_no,
                'total_ord_no':total_ord_no,
                # 'total_order_value':format(total_order_value['order_total__sum'],".2f"),
                'total_order_value':round(total_order_value['order_total__sum'],2),
                # 'avg_ord_value':format(avg_ord_value['average_order_value'],".2f"),
                'avg_ord_value':round(avg_ord_value['average_order_value'],2)
                # 'latest_order': latest_order,
                
                }
            return render(request,'mycartadmin/index.html', context)
        else:
            messages.error(request,"You have no admin privileges to view this page")
            return redirect('home')
    else:
        return redirect('admin_login')
    
    



def admin_page_view(request):
    if request.method == "POST":
        
        username        = request.POST['email']
        password        = request.POST['password']
        admin_user      = authenticate(username=username, password=password)
        

        if admin_user is not None:
            
            if admin_user.is_superuser:
               
                login(request,admin_user)
                
                return redirect('admin_login')
            else:
               
                messages.error(request,"Only Admin can access this page.")
                return redirect('admin_login')
        else:
            messages.error(request,"The login details given are not of any admin user. Please retry with correct details.")
            return redirect('admin_login')
    else:

        return redirect('admin_login')


@login_required(login_url='admin_login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_logout(request):

    logout(request)
   
    return redirect('admin_login')


#rendering various pages on the admin panel
@login_required(login_url='admin_login')
def usermanage(request):
    users = Account.objects.all().order_by('-date_joined')
    # paginator = Paginator(users, 5) # Show 25 contacts per page.
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)

   
    
   
    return render(request,'mycartadmin/usermanage.html',{'users':users})


@login_required(login_url='admin_login')
def admin_category(request):
    category = Category.objects.all().order_by("id")
    
    return render(request,'mycartadmin/category.html',{'categories':category})

@login_required(login_url='admin_login')
def admin_product(request):
    product = Product.objects.all().order_by("id")
   
    return render(request,'mycartadmin/product.html',{'products':product})

@login_required(login_url='admin_login')
def delete_category(request,id):
    category = Category.objects.get(id=id)
    category.delete()
    return redirect('admin_category')




def edit_product(request,id):
    instance = get_object_or_404(Product, id=id)
    form = ProductForm(request.POST or None, instance=instance)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request,'Product has been updated')
            return redirect('admin_product')
        else:  
            context = {
                'form'     : form,
                'product':instance,
                }
            return render(request, 'mycartadmin/edit_product.html',context)
    else:  
        context = {
            'form'     : form,
            'product':instance,
            }
        return render(request, 'mycartadmin/edit_product.html',context)

def edit_category(request,id):
    instance = get_object_or_404(Category, id=id)
    form = CategoryForm(request.POST or None, instance=instance)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request,'Category has been updated')
            return redirect('admin_category')
        else:  
            context = {
                'form'     : form,
                'category': instance,
                }
            return render(request, 'mycartadmin/edit_category.html',context)
    else:  
        context = {
            'form'     : form,
            'category': instance,
            }
        return render(request, 'mycartadmin/edit_category.html',context)






@login_required(login_url='admin_login')
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            
            product_name = form.cleaned_data['product_name']
            slug = slugify(product_name)
           
            description = form.cleaned_data['description']
            price = form.cleaned_data['price']
            images = form.cleaned_data['images']
            stock = form.cleaned_data['stock']
            is_available = form.cleaned_data['is_available']
            category = form.cleaned_data['category']
            
            product = Product.objects.create(product_name=product_name, slug=slug, description=description,price=price,mrp_price=price,images=images,stock=stock,is_available=is_available,category=category)
            product.save()
            messages.success(request,'Product added successfully')
            return redirect('add_product')
        else:
            messages.error(request,'form not valid')
            form = ProductForm(request.POST or None, request.FILES or None)
            context = {
            'form':form
            }
            return render(request,'mycartadmin/add_product.html',context)
    else:
        form = ProductForm()
  
        context = {
            'form':form
        }
        return render(request,'mycartadmin/add_product.html',context)



@login_required(login_url='admin_login')
def add_category(request):
    form = CategoryForm(request.POST or None, request.FILES or None)
    if request.method == "POST":
      
        
       
        if form.is_valid():
            
            category_name = form.cleaned_data['category_name']
            slug = slugify(category_name)
            
            description = form.cleaned_data['description']
            category_image = form.cleaned_data['category_image']
            
        
            
            category = Category.objects.create(category_name=category_name, slug=slug, description=description,category_image=category_image)
            category.save()
            messages.success(request,'category added successfully')
            return redirect('add_category')
        else:
            messages.error(request,'form not valid')
            
            context = {
            'form':form
            }
            return render(request,'mycartadmin/add_category.html',context)
    else:
       
        
        context = {
            'form':form
        }
        return render(request,'mycartadmin/add_category.html',context)

@login_required(login_url='admin_login')
def sales_report(request):
    
    orders = Order.objects.all().order_by('-order_number')
   

    context = {
        'orders':orders,
          
    }

    return render(request,'mycartadmin/sales_report.html',context)


@login_required(login_url='admin_login')
def admin_orders(request):
    
    orders = Order.objects.all().order_by('-order_number')
    form = OrderStatusForm()
    
    
    paginator = Paginator(orders, 10) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    context = {
        'orders':orders,
        'form':form,
        
    }

    return render(request,'mycartadmin/orders.html',context)

@login_required(login_url='admin_login')
def admin_offers(request):
    coupon_offers = Coupon.objects.all().order_by('-valid_to')
    prod_offers = ProductOffer.objects.all().order_by('-valid_to')
    cat_offers = CategoryOffer.objects.all().order_by('-valid_to')


    paginator = Paginator(coupon_offers, 5) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    context = {
        'coupon_offers': page_obj,
        'prod_offers': prod_offers,
        'cat_offers': cat_offers,

    }

    return render(request,'mycartadmin/offers.html',context)

#functions on userpage - edit, block, delete.

@login_required(login_url='admin_login')
def admin_user_deactivate(request):
    id = request.GET['id']
 
    user = Account.objects.get(id=id)
    user.is_active = False
    user.save()

    return JsonResponse({'success':'deactivation completed'})


@login_required(login_url='admin_login')
def admin_user_activate(request):
    username = request.GET['username']
    user = Account.objects.get(username = username)
    user.is_active = True
    user.save()
    return JsonResponse({'success':'user activated'})

@login_required(login_url='admin_login')
def admin_user_edit(request,id):
    user = Account.objects.get(id=id)
    # user.is_active = True
    # user.save()
    return render('login_view')
    
@login_required(login_url='admin_login')
def admin_user_delete(request):
    id = request.GET['id']
    user = Account.objects.get(id=id)
    user.delete()
    return JsonResponse({'success':'user deleted successfully'})

# @login_required(login_url='admin_login')
# def update_order_status(request,order_no):
#     order = Order.objects.get(order_number = order_no)
#     print('received order status update request')
    
#     form = OrderStatusForm(request.POST)
#     if form.is_valid():
#         status = request.POST['status']
#         print(status)
#         order.status = status
#         order.save()
#     print(status)
#     print(order)
    
#     return redirect ('admin_orders')

@login_required(login_url='admin_login')
def update_order_status(request, order_no):

    instance = get_object_or_404(Order, order_number = order_no)

    form = OrderStatusForm(request.POST or None, instance=instance)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request,'Order Status has been updated')
            return redirect('admin_orders')
    else:  
        context = {
            'form'     : form,
            'order': instance,
            }
        return render(request, 'mycartadmin/update_order_status.html',context)




def add_banner(request):
    form = BannerUpdateForm(request.POST or None, request.FILES or None)
  
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('admin_banners')
        else:
            messages.error(request,'form not valid')            
            context = {
            'form':form
            }
            return render(request,'mycartadmin/add_banner.html',context)
    else:
        context = {
            'form':form
        }
        return render(request,'mycartadmin/add_banner.html',context)

# OFFERS SECTION

# coupon offers
def add_coupon(request):
    form = CouponApplyForm(request.POST or None, request.FILES or None)  
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('admin_offers')
        else:
            messages.error(request,'form not valid')            
            context = {
            'form':form
            }
            return render(request,'mycartadmin/add_coupon.html',context)
    else:
        context = {
            'form':form
        }
        return render(request,'mycartadmin/add_coupon.html',context)
    
    
def edit_coupon(request,c_id):
    instance = get_object_or_404(Coupon, id=c_id)
    form = CouponApplyForm(request.POST or None, instance=instance)


    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request,'Product has been updated')
            return redirect('admin_offers')
        else:
             context = {
            'form'     : form,
            'coupon':instance,
            }
        return render(request, 'mycartadmin/edit_coupon_offer.html',context)
    else:  
        context = {
            'form'     : form,
            'coupon':instance,
            }
        return render(request, 'mycartadmin/edit_coupon_offer.html',context)
    


def activate_coupon(request):
    coupon_id = request.GET['couponId']
    coupon = Coupon.objects.get(id = coupon_id)
    coupon.active = True
    coupon.save()

    return redirect('admin_offers')

def block_coupon(request):
  
    coupon_id = request.GET['couponId']
    coupon = Coupon.objects.get(id = coupon_id)
    coupon.active = False
    coupon.save()

    return redirect('admin_offers')

def delete_coupon(request):
    coupon_id = request.GET['couponId']
    coupon = Coupon.objects.get(id = coupon_id)
    
    coupon.delete()

    return redirect('admin_offers')




# Product offers
def add_product_offer(request):

    form = ProductOfferForm(request.POST or None, request.FILES or None)  
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('admin_offers')
        else:
            messages.error(request,'form not valid')            
            context = {
            'form':form
            }
            return render(request,'mycartadmin/add_product_offer.html',context)
    else:
        context = {
            'form':form
        }
        return render(request,'mycartadmin/add_product_offer.html',context)
    
    
    
def edit_product_offer(request,prod_id):
    instance = get_object_or_404(ProductOffer, id=prod_id)
    form = ProductOfferForm(request.POST or None, instance=instance)


    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request,'Offer has been updated')
            return redirect('admin_offers')
        else:
             context = {
            'form'     : form,
            'coupon':instance,
            }
        return render(request, 'mycartadmin/edit_product_offer.html',context)
    else:  
        context = {
            'form'     : form,
            'coupon':instance,
            }
        return render(request, 'mycartadmin/edit_product_offer.html',context)



def activate_product_offer(request):
    offer_id = request.GET['proOffId']
   
    offer = ProductOffer.objects.get(id = offer_id)

    offer.is_active = True
    offer.save()

    return redirect('admin_offers')

def block_product_offer(request):
    offer_id = request.GET['proOffId']
    offer = ProductOffer.objects.get(id = offer_id)
    offer.is_active = False
    offer.save()

    return redirect('admin_offers')

def delete_product_offer(request):
    offer_id = request.GET['proOffId']
    offer = ProductOffer.objects.get(id = offer_id)
    
    offer.delete()

    return redirect('admin_offers')

# Category offers
def add_cat_offer(request):

    form = CategoryOfferForm(request.POST or None, request.FILES or None)  
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('admin_offers')
        else:
            messages.error(request,'form not valid')            
            context = {
            'form':form
            }
            return render(request,'mycartadmin/add_cat_offer.html',context)
    else:
        context = {
            'form':form
        }
        return render(request,'mycartadmin/add_cat_offer.html',context)
    
    
def edit_cat_offer(request,cat_id):
    instance = get_object_or_404(CategoryOffer, id=cat_id)
    form = CategoryOfferForm(request.POST or None, instance=instance)
  

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request,'Offer has been updated')
            return redirect('admin_offers')
        else:
             context = {
            'form'     : form,
            'coupon':instance,
            }
        return render(request, 'mycartadmin/edit_cat_offer.html',context)
    else:  
        context = {
            'form'     : form,
            'coupon':instance,
            }
        return render(request, 'mycartadmin/edit_cat_offer.html',context)

def activate_cat_offer(request):
    offer_id = request.GET['catOffId']
    
    offer = CategoryOffer.objects.get(id = offer_id)
 
    offer.is_active = True
    offer.save()

    return redirect('admin_offers')

def block_cat_offer(request):
    offer_id = request.GET['catOffId']
    offer = CategoryOffer.objects.get(id = offer_id)
    offer.is_active = False
    offer.save()

    return redirect('admin_offers')

def delete_cat_offer(request):
    offer_id = request.GET['catOffId']
    offer = CategoryOffer.objects.get(id = offer_id)
    
    offer.delete()

    return redirect('admin_offers')



def add_gallery_images(request,id):
    instance = get_object_or_404(Product, id=id)
    form = ProductGalleryForms(request.POST or None, request.FILES or None, instance=instance)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request,'Image gallery has been updated')
            return redirect('admin_product')
        else:
             context = {
            'form'     : form,
            }
        return render(request, 'mycartadmin/add_gallery_images.html',context)
    else:  
        context = {
            'form'     : form,
            }
        return render(request, 'mycartadmin/add_gallery_images.html',context)