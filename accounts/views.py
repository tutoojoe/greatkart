from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import RegistrationForm
from accounts.models import Account, Otp
from carts.models import Cart,CartItem
from carts.views import _cart_id
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required

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
            return redirect ('register')
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
        
            return redirect('verify_otp')
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




    return render(request, 'accounts/dashboard.html')


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
        
        user = Account.objects.filter(email=user_email)
        for i in user:
            user_mobile = i.mobile_number
        
        print(user_mobile)

        otp_number = random.randint(100000,999999)
        auth_sid = "AC4a47f577c35cc44a86aab76e62e7d754"
        auth_token = "44694e787e5181806dc94b84eafb6791"
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
       

