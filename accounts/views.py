from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from .forms import RegistrationForm,AddAddressForm,UserProfileForm, Userform
from accounts.models import Account, Otp, Address, UserProfile
from carts.models import Cart,CartItem
from carts.views import _cart_id
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from orders.models import Order, OrderProduct
from .private import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN
from django.core.paginator import Paginator

#verificationemail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
import requests
from twilio.rest import Client
import random

# Create your views here.
def add_address(request):
    if request.user.is_authenticated:            
        if request.method == "POST":
            print("Got a POST request")
            form = AddAddressForm(request.POST)
            print("checking the form validation")
            if form.is_valid():
                print("Validation done collectiong, collecting data")
                user = Account.objects.get(id = request.user.id)
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                address_line_1 = form.cleaned_data['address_line_1']
                address_line_2 = form.cleaned_data['address_line_2']
                mobile = form.cleaned_data['mobile']
                email = form.cleaned_data['email']
                city = form.cleaned_data['city']
                district = form.cleaned_data['district']
                state = form.cleaned_data['state']
                country = form.cleaned_data['country']
                pincode = form.cleaned_data['pincode']
                
                address = Address.objects.create(user=user,first_name=first_name,last_name=last_name,address_line_1=address_line_1,address_line_2=address_line_2, email=email, mobile=mobile, city=city, state=state, district=district, country=country, pincode=pincode)
                print("going to save address")
                address.save()
                print("address saved")       

                messages.success(request,"Your address has been registered. ")
                return redirect ('checkout')
        else:
            form = AddAddressForm()    
            context = {
                    'form':form
            }
            return render(request, 'accounts/add_address.html', context)
    else:
        return redirect('login')

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            mobile_number = form.cleaned_data['mobile_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]

            user = Account.objects.create_user(first_name=first_name,last_name=last_name,email=email, mobile_number=mobile_number, username = username, password=password)
            user.save()

            # create user_profile
            profile = UserProfile()
            profile.user_id = user.id
            profile.profile_picture = 'default/default-user.png'
            profile.save()


            #user activation
            # current_site = get_current_site(request)
            # mail_subject = 'Please activate your account'
            # message = render_to_string('accounts/account_verification_email.html', {
            #     'user': user,
            #     'domain':current_site,
            #     'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token':default_token_generator.make_token(user),
            # })
            # to_email = email
            # send_email = EmailMessage(mail_subject,message,to=[to_email])
            # send_email.send()
            # return redirect ('accounts/login/?command=verification&mail='+email)

            messages.success(request,"Thank you for registering with us. ")
            return redirect ('login')
    else:
        form = RegistrationForm()    
    context = {
            'form':form
    }

    return render(request, 'accounts/register.html', context)

def login(request):
    if request.method =="POST":
        email       = request.POST['email']
        password    = request.POST['password']

        user =  auth.authenticate(email = email, password = password)

        print("user details are:-", user)
        request.session['user_email'] = email
        user_email = request.session['user_email']
        print('user email is', user_email)

        if user is not None:
            try:
                cart    = Cart.objects.get(cart_id = _cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart = cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)
                    product_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))
                    
                    # get the cart items from the user to access his product variations.
                    cart_item           = CartItem.objects.filter(user=user)           
                    ex_var_list = []
                    id = []
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)
                    
                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user   = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()
                        
            except:
                pass
            auth.login(request,user)
            return redirect('verify_otp')
            # return redirect('home')
        else:
            messages.error(request,"Invalid Credentials")
            return redirect('login')
    return render(request, 'accounts/login.html')

@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request,"You are logged out..!")
    return redirect('login')

def activate(request,uidb64,token ):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request,'Congratulations, your account is activated. ')
        return redirect('login')
    else:
        messages.error(request,'Invalid activation link')

    return redirect('register')


@login_required(login_url = 'login')
def dashboard(request):

    orders = Order.objects.order_by('-created_at').filter(user_id = request.user.id, is_ordered = True)
    orders_count = orders.count()

    userprofile = UserProfile.objects.get(user_id = request.user.id)
    context = {
        'orders_count':orders_count,
        'userprofile':userprofile,
    }


    return render(request, 'accounts/dashboard.html',context)


def verify_otp(request):
    if request.method == "POST":
        generated_otp = request.POST['generated_otp']
        otp_input = request.POST['otp_input']
        print(generated_otp,"|",otp_input)
        if generated_otp == otp_input:
            messages.success(request,"OTP verified successfully.")
            user_email = request.session['user_email']
            
            print(user_email)
            
            user = Account.objects.get(email=user_email)
            print(user)
            

            auth.login(request,user)
            print('signing in')
            return redirect('home')
        else:
            return redirect('login')
    else:
        print('request to generate OTP')
        user_email = request.session['user_email']
        print(user_email)
        
        user = Account.objects.filter(email=user_email)
        for i in user:
            user_mobile = i.mobile_number
        
        print(user_mobile)

        otp_number = random.randint(100000,999999)
        auth_sid = TWILIO_ACCOUNT_SID
        auth_token = TWILIO_AUTH_TOKEN
        otp_client = Client(auth_sid,auth_token)
        otp_message = otp_client.messages.create(
            body = "Your OTP number is "+str(otp_number),
            from_ = "+13097221372",
            to = "+91"+user_mobile
        )
        context = {
            'otp_number':otp_number,
            }
        return render(request,'accounts/login_otp.html',context)
       
@login_required(login_url='login')
def my_orders(request):
    orders = Order.objects.filter(user = request.user,is_ordered=True).order_by('-created_at')

    paginator = Paginator(orders, 5) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    print(paginator.count)
    print(paginator.num_pages)
    context = {
        'orders': page_obj,
        }
 
    return render(request, 'accounts/my_orders.html', context)


@login_required(login_url='login')
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile,user = request.user)

    if request.method == "POST":
        user_form           = Userform(request.POST, instance=request.user)
        profile_form   = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'Your profile has been updated')
            return redirect('edit_profile')
    else:
        user_form = Userform(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
        'user_form'     : user_form,
        'profile_form'  : profile_form,
        'userprofile'   :userprofile
    }

    return render(request, 'accounts/edit_profile.html',context)

@login_required(login_url='login')
def change_password(request):

    if request.method == "POST":
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(username__exact = request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                # auth.logout(request) django will log out by default
                messages.success(request,'Password Updated Sucessfully')
                return redirect('change_password')
            else:
                messages.error(request, 'You have entered the wrong password')
                return redirect('change_password')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('change_password')

    return render (request, 'accounts/change_password.html')

@login_required(login_url='login')
def order_detail(request,order_id):
    print('order detail req recvd')
    order_detail = OrderProduct.objects.filter(order__order_number = order_id)
    order = Order.objects.get(order_number = order_id)
    print('both details fetced')
    sub_total = 0
    for i in order_detail:
        sub_total += i.product_price * i.quantity
    context = {
        'order_detail':order_detail,
        'order':order,
        'sub_total': sub_total,
    }
    return render (request, 'accounts/order_detail.html',context)


def my_addresses(request):

    addresses = Address.objects.filter(user = request.user.id).order_by('-id')
    context = {
        "addresses":addresses,
    }

    return render(request,'accounts/my_addresses.html',context)

def delete_address(request,add_id):
    print(add_id)
    
    del_add = Address.objects.filter(user = request.user.id, id= add_id)

    del_add.delete()

    addresses = Address.objects.filter(user = request.user.id).order_by('-id')
    context = {
        "addresses":addresses,
    }
    return render(request,'accounts/my_addresses.html', context)