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
from orders.forms import OrderForm, OrderStatusForm
from store.forms import ProductForm
from category.forms import CategoryForm
from store.models import Product
from orders.models import Order
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
    print('received the filter list')
    if request.method == "POST":
        print('Post request')
        from_date = request.POST["from_date"]
        to_date = request.POST["to_date"]
        orders = Order.objects.filter(created_at__range=(from_date, to_date))

    for order in orders:
        data.append([str(order.first_name),str(order.order_number),str(order.phone),str(order.order_total)])

    print(data)

    fileName = 'orders.pdf'

    pdf = SimpleDocTemplate(
        fileName,
        pagesize = letter,
    )

    table = Table(data)
    print('going to print the data')
    style = TableStyle([
        ('BACKGROUND',(0,0),(4,0),colors.green),
        ('TESTCOLOR',(0,0),(-1,0),colors.whitesmoke),
        # ('ALIGN',(0,0),(-1,-1),'CENTER'),
        # ('ALIGN',(1,0),(-1,-1),'CENTER'),
        ('FONTNAME',(0,0),(-1,0),'Courier-Bold'),
        ('FONTSIZE',(0,0),(-1,0),14),
        
        ('BOTTOMPADDING',(0,0),(-1,0),12),
        ('BACKGROUND',(0,1),(-1,-1),colors.beige),
    ])
    table.setStyle(style)


    elems = []
    elems.append(table)
    pdf.build(elems)

    return redirect('admin_orders')
    
    


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
        print('Post request')
        from_date = request.POST["from_date"]
        to_date = request.POST["to_date"]
        orders = Order.objects.filter(created_at__range=(from_date, to_date))

    for order in orders:
        lines.append([str(order.first_name),str(order.order_number),str(order.phone),str(order.order_total)])

    print(lines)
  
    # filename = 'orders.pdf'






    # from here the old items start
    for line in lines:
        textobj.textLine(str(line))


    c.drawText(textobj)
    c.showPage()
    c.save()
    buf.seek(0)


    return FileResponse(buf, as_attachment=True,filename='filtered_orders.pdf')




# Create your views here.
def admin_login(request):
        print('received a GET request in login')
        if request.user.is_authenticated:
            if request.user.is_superuser:
                print('authenticated user logging in')
                return redirect('admin_dashboard')
            else:
                messages.error(request, "You dont have admin privileges to view this page.")
                return redirect('home')
        else:
            print('unauthoried user - diverted to loginpage')
            return render(request,'mycartadmin/login.html')

@login_required(login_url='admin_login')
def admin_dashboard(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            print('user is a superuser')
            total_ord_no = Order.objects.all().count()
            total_user_no = Account.objects.all().count()
            print(total_ord_no,'orders')
            print(total_user_no,'users')
            total_order_value = Order.objects.all().aggregate(Sum('order_total'))
            print(total_order_value['order_total__sum'],'total order value')

            avg_ord_value = Order.objects.all().aggregate(average_order_value = Avg('order_total'))
            print(avg_ord_value,)
            val_diff = Order.objects.aggregate(value_diff = Max('order_total', output_field = FloatField())-Avg('order_total'))
            print(val_diff,)

            # orders_per_day = Order.objects.all().extra({'date_created' : "date(created_at)"}).values('created_at').annotate(created_count=Count('id'))
            orders_per_day = Order.objects.annotate(order_day=Trunc('created_at', 'day', output_field=DateTimeField())).values('order_day').annotate(orders=Count('id')).order_by('-order_day')[:7]
            ord_val_per_day = Order.objects.annotate(order_day=Trunc('created_at', 'day', output_field=DateTimeField())).values('order_total').annotate(ord_value=Sum('id')).order_by('-order_day')[:7]
            

            labels = []
            ord_data = []
            val_data = []


            for ord in orders_per_day:
                print(ord['order_day'], ord['orders'])
                labels.append(str(ord['order_day'].date()))
                ord_data.append(ord['orders'])

            for val in ord_val_per_day:
                val_data.append(int(val['ord_value']))
            
        
            labels.reverse()
            # val_data.reverse()
            ord_data.reverse()
            print(val_data)
            print(labels)   
            print(ord_data)

            context = {
                'labels':labels,
                'data':ord_data,
                'val_data':val_data,
                'total_user_no':total_user_no,
                'total_ord_no':total_ord_no,
                'total_order_value':format(total_order_value['order_total__sum'],".2f"),
                'avg_ord_value':format(avg_ord_value['average_order_value'],".2f"),
                
                }
            return render(request,'mycartadmin/index.html', context)
        else:
            messages.error(request,"You have no admin privileges to view this page")
            return redirect('home')
    else:
        return redirect('admin_login')

@login_required(login_url='admin_login')
def admin_page_view(request):
    if request.method == 'POST':
        username        = request.POST['email']
        password        = request.POST['password']
        admin_user      = authenticate(username=username, password=password)
        print('user authenticated')

        if admin_user is not None:
            print('valid admin found, redirecting to login')
            if admin_user.is_superuser:
                print('admin user is superuser> Logging in..')
                login(request,admin_user)
                print('superuser authenticated and logged in.')
                return redirect('admin_login')
            else:
                print('The user is not superuser. No login permission. Sending Error Message')
                messages.error(request,"Only Admin can access this page.")
                return redirect('admin_login')
        else:
            messages.error(request,"The login details given are not of any admin user. Please retry with correct details.")
            return redirect('admin_login')
    else:
        print('Initial GET request. Not authenticated, redirecting to Login')
        return redirect('admin_login')


@login_required(login_url='admin_login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_logout(request):
    print('Logout requesst received')
    logout(request)
    print('User successfully logged out')
    return redirect('admin_login')


#rendering various pages on the admin panel
@login_required(login_url='admin_login')
def usermanage(request):
    users = Account.objects.all().order_by('-date_joined')
    # paginator = Paginator(users, 5) # Show 25 contacts per page.
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)

   
    
    print('Entering User Manage page')
    return render(request,'mycartadmin/usermanage.html',{'users':users})

@login_required(login_url='admin_login')
def admin_category(request):
    category = Category.objects.all().order_by("id")
    print('Entering Category Manage page')
    return render(request,'mycartadmin/category.html',{'categories':category})

@login_required(login_url='admin_login')
def admin_product(request):
    product = Product.objects.all().order_by("id")
    print('Entering Product Manage page')
    return render(request,'mycartadmin/product.html',{'products':product})


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






@login_required(login_url='admin_login')
def add_product(request):
    if request.method == "POST":
        print('post request')
        form = ProductForm(request.POST or None, request.FILES or None)
        print('got form, going fo validity check')
        if form.is_valid():
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
            
            product = Product.objects.create(product_name=product_name, slug=slug, description=description,price=price,images=images,stock=stock,is_available=is_available,category=category)
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
        print('Entering Product Manage page')
        context = {
            'form':form
        }
        return render(request,'mycartadmin/add_product.html',context)



@login_required(login_url='admin_login')
def add_category(request):
    form = CategoryForm(request.POST or None, request.FILES or None)
    if request.method == "POST":
        print('post request')
        
        print('got form, going fo validity check')
        if form.is_valid():
            print('form valid')
            category_name = form.cleaned_data['category_name']
            slug = slugify(category_name)
            print(slug)
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
       
        print('Entering add category page')
        context = {
            'form':form
        }
        return render(request,'mycartadmin/add_category.html',context)




@login_required(login_url='admin_login')
def admin_orders(request):
    
    orders = Order.objects.all().order_by('-order_number')
    form = OrderStatusForm()
    
    
    paginator = Paginator(orders, 10) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    context = {
        'orders':page_obj,
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

    print(paginator.count)
    print(paginator.num_pages)
    context = {
        'coupon_offers': page_obj,
        'prod_offers': prod_offers,
        'cat_offers': cat_offers,

    }

    print('Entering Offer Manage page')
    return render(request,'mycartadmin/offers.html',context)

#functions on userpage - edit, block, delete.

@login_required(login_url='admin_login')
def admin_user_deactivate(request):
    id = request.GET['id']
    print(id)
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

@login_required(login_url='admin_login')
def update_order_status(request,order_no):
    order = Order.objects.get(order_number = order_no)
    print('received order status update request')
    
    form = OrderStatusForm(request.POST)
    if form.is_valid():
        status = request.POST['status']
        print(status)
        order.status = status
        order.save()
    print(status)
    print(order)
    
    return redirect ('admin_orders')
