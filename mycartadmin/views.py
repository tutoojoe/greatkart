from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from category.models import Category
from orders.forms import OrderForm, OrderStatusForm
from store.models import Product
from orders.models import Order
from accounts.models import Account
import mycartadmin

# Create your views here.
def admin_login(request):
        print('received a GET request in login')
        if request.user.is_authenticated:
            print('authenticated user logging in')
            return render(request, 'mycartadmin/index.html')
        else:
            print('unauthoried user - diverted to loginpage')
            return render(request,'mycartadmin/login.html')
            


def admin_page_view(request):
    if request.method == 'POST':
        print('received a POST request')
        username        = request.POST['email']
        password        = request.POST['password']
        print('got username and password')
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
            return redirect('admin_login')
    else:
        print('Initial GET request. Not authenticated, redirecting to Login')
        return redirect('admin_login')


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_logout(request):
    print('Logout requesst received')
    logout(request)
    print('User successfully logged out')
    return redirect('admin_login')


#rendering various pages on the admin panel
@login_required
def usermanage(request):
    users = Account.objects.all()
    
    print('Entering User Manage page')
    return render(request,'mycartadmin/usermanage.html',{'users':users})

@login_required
def admin_category(request):
    category = Category.objects.all().order_by("id")
    print('Entering Category Manage page')
    return render(request,'mycartadmin/category.html',{'categories':category})

@login_required
def admin_product(request):
    product = Product.objects.all().order_by("id")
    print('Entering Product Manage page')
    return render(request,'mycartadmin/product.html',{'products':product})

@login_required
def admin_orders(request):
    orders = Order.objects.all().order_by('-order_number')
    form = OrderStatusForm()
    context = {
        'orders':orders,
        'form':form,
    }
    print('Entering Order Manage page')
    return render(request,'mycartadmin/orders.html',context)

@login_required
def admin_offers(request):
    print('Entering Offer Manage page')
    return render(request,'mycartadmin/offers.html')

#functions on userpage - edit, block, delete.

@login_required
def admin_user_deactivate(request,id):
    user = Account.objects.get(id=id)
    user.is_active = False
    user.save()
    return redirect(usermanage)

@login_required
def admin_user_activate(request,username):
    user = Account.objects.get(username = username)
    user.is_active = True
    user.save()
    return redirect(usermanage)

@login_required
def admin_user_edit(request,id):
    user = Account.objects.get(id=id)
    # user.is_active = True
    # user.save()
    return render('login_view')
    
@login_required 
def admin_user_delete(request,id):
    user = Account.objects.get(id=id)
    user.delete()
    return redirect(usermanage)


def update_order_status(request,order_no):
    order = Order.objects.get(order_number = order_no)
    
    form = OrderStatusForm(request.POST)
    if form.is_valid():
        status = request.POST['status']
        order.status = status
        order.save()
    print(status)
    print(order)
    
    return redirect ('admin_orders')
