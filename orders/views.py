from typing import ContextManager
from django.http.response import HttpResponse, JsonResponse
from accounts.models import Address
from carts.models import CartItem
from store.models import Product
from .forms import OrderForm,Order, OrderStatusForm
from django.shortcuts import redirect, render
import datetime
import razorpay
from store.models import Product
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from orders.models import Order, Payment, OrderProduct
import json
from django.core.mail import EmailMessage
from django.template.loader import render_to_string



# Create your views here.
def place_order(request, total=0, quantity=0):
    print('Order place request received')
    current_user = request.user
    #if the cart count is <=0, redirect to store

    cart_items = CartItem.objects.filter(user = current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')
    

    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total   += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (5 * total)/100
    grand_total = total + tax
    print('going to check the post request')
    if request.method == "POST":
        # form = OrderForm(request.POST)
        # print(form)
        print('POST request - going to validate')
        # if form.is_valid():
        print('form validated, getting to the fields')
        #store all the billing information inside the table
        address_id = request.POST['ship_address']
        print(address_id)
        address = Address.objects.filter(id = address_id, user = request.user.id)
        for i in address:
            first_name = i.first_name
            last_name = i.last_name
            mobile = i.mobile
            email = i.email
            address_line_1 = i.address_line_1
            address_line_2 = i.address_line_2
            country = i.country
            state = i.state
            city = i.district
        print('collected details going to assign')
        data = Order()
        data.user           = current_user
        data.first_name     = first_name
        data.last_name      = last_name
        data.phone          = mobile
        data.email          = email
        data.address_line_1 = address_line_1
        data.address_line_2 = address_line_2
        data.country        = country
        data.state          = state
        data.city           = city
        data.order_note     = request.POST['order_note']
        data.order_total    = grand_total
        data.tax            = tax
        data.ip             = request.META.get('REMOTE_ADDR')
        print('Assigned all the values and going to save')
        data.save()

         #generate order no
        yr                  = int(datetime.date.today().strftime('%Y'))
        dt                  = int(datetime.date.today().strftime('%d'))
        mt                  = int(datetime.date.today().strftime('%m'))
        d                   = datetime.date(yr,mt,dt)
        current_date        = d.strftime("%Y%m%d")

        order_number        = current_date + str(data.id)
        print('order number generated')
        data.order_number   = order_number
        data.save()
        print('details verified and directed to checkout')
        
        order               = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
        print('order value selected and passed to context')

        context             = {
            'order' : order,
            'cart_items' : cart_items,
            'total' : total,
            'tax' : tax,
            'grand_total' : grand_total,
        }
        return render(request,'orders/payments.html',context)
    else:
        print('entered else case/GET case and redirecting to checkout')
        return redirect('checkout')



def payments(request):
    
    body = json.loads(request.body)
    order = Order.objects.get(user = request.user, is_ordered = False, order_number = body['orderID'])
    print(body)
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],
    )
    payment.save()
    order.payment = payment 
    order.is_ordered = True
    order.save()

    # move the cart products to the ordered products table
    cart_items = CartItem.objects.filter(user = request.user)
    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

        #for variation - Many to Many field, first save data and then update.
        cart_item = CartItem.objects.get(id = item.id)
        product_variation = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id = orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()
        
    # reduce the quantity of sold products
        product = Product.objects.get(id = item.product_id)
        product.stock -= item.quantity
        product.save()

    # clear the cart and send order received confirmation to customer
    CartItem.objects.filter(user=request.user).delete()

    # sending emails to user    
    mail_subject = 'Thank you for your order..!!'
    message = render_to_string('orders/order_received_email.html', {
        'user': request.user,
        'order':order,
        
    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject,message,to=[to_email])
    send_email.send()

    # send data to JSON response
    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
        }

    return JsonResponse(data)

razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
def proceed_payment(request,order_id):
    order = Order.objects.filter(order_number = order_id)
    print(order)
    
    for i in order:
        first_name = i.first_name
        last_name = i.last_name
        phone = i.phone
        email = i.email
        total = i.order_total * 100
        order_number = i.order_number
        print(first_name,'first name')
        print(total,'total')
        print(order_number,"order number")

       

    data = { 
        "amount": total, 
        "currency": "INR", 
        "receipt": order_number,
        
        }
    
    payment = razorpay_client.order.create(data=data)
    context = {
        'payment':payment,
        'order':order,
        'total':total,
        'first_name' :first_name,
        'last_name' :last_name,
        'phone' :phone,
        'email' :email,
        "order_number":order_number,
        
    }

    return render(request,'orders/proceed_payment.html',context)


def order_complete(request):
    print("payment completed and saving")
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')
    print(order_number,"- order No &", transID, "- Trans ID")

    try:
        order = Order.objects.get(order_number = order_number, is_ordered = True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)

        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity


        payment = Payment.objects.get(payment_id = transID)

        context = {
            'order':order,
            'ordered_products' : ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal':subtotal,
        }
        return render(request, 'orders/order_complete.html',context)


    except (Payment.DoesNotExist, Order.DoesNotExist):

        print("payment feedback not received. exiting without saving")
        return redirect('home')


def rzp_order_complete(request):
    print("payment completed and saving")
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')
    print(order_number,"- order No &", transID, "- Trans ID")
    order = Order.objects.get(user = request.user, is_ordered = False, order_number = order_number)
    print(order)
    payment = Payment(
        user = request.user,
        payment_id = transID,
        payment_method = "Razor Pay",
        amount_paid = order.order_total,
        status = "COMPLETED",
        )
    payment.save()
    order.payment= payment 
    order.is_ordered = True
    order.save()

    cart_items = CartItem.objects.filter(user = request.user)
    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

        #for variation - Many to Many field, first save data and then update.
        cart_item = CartItem.objects.get(id = item.id)
        product_variation = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id = orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()
        
    # reduce the quantity of sold products
        product = Product.objects.get(id = item.product_id)
        product.stock -= item.quantity
        product.save()

    # clear the cart and send order received confirmation to customer
    CartItem.objects.filter(user=request.user).delete()

    # sending emails to user    
    mail_subject = 'Thank you for your order..!!'
    message = render_to_string('orders/order_received_email.html', {
        'user': request.user,
        'order':order,
        
    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject,message,to=[to_email])
    send_email.send()
    
    try:
        print("trying order ID")
        order = Order.objects.get(order_number = order_number)
        print("fetched order ")
        ordered_products = OrderProduct.objects.filter(order_id=order.id)
        subtotal = 0
        for i in ordered_products:
            # prod_total = i.product_price * i.quantity
            subtotal += i.product_price * i.quantity


        # payment = Payment.objects.get(payment_id = transID)

        context = {
            # 'prod_total': prod_total,
            'order':order,
            'ordered_products' : ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal':subtotal,
        }
        CartItem.objects.filter(user=request.user).delete()
        return render(request, 'orders/order_complete.html',context)


    except (Payment.DoesNotExist, Order.DoesNotExist):

        print("payment feedback not received. exiting without saving")
        return redirect('home')

def cod_order_complete(request,order_number):
    print("COD requet received")
    
    order = Order.objects.get(user = request.user, is_ordered = False, order_number = order_number)
    print(order)
    payment = Payment(
        user = request.user,
        payment_id = "COD - Payement pending",
        payment_method = "COD",
        amount_paid = order.order_total,
        status = "COD",
        )
    payment.save()
    order.payment= payment 
    order.is_ordered = True
    order.save()

    cart_items = CartItem.objects.filter(user = request.user)
    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

        #for variation - Many to Many field, first save data and then update.
        cart_item = CartItem.objects.get(id = item.id)
        product_variation = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id = orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()
        
    # reduce the quantity of sold products
        product = Product.objects.get(id = item.product_id)
        product.stock -= item.quantity
        product.save()

    # clear the cart and send order received confirmation to customer
    CartItem.objects.filter(user=request.user).delete()

    # sending emails to user    
    mail_subject = 'Thank you for your order..!!'
    message = render_to_string('orders/order_received_email.html', {
        'user': request.user,
        'order':order,
        
    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject,message,to=[to_email])
    send_email.send()
    
    try:
        print("trying order ID")
        order = Order.objects.get(order_number = order_number)
        print("fetched order ")
        ordered_products = OrderProduct.objects.filter(order_id=order.id)
        subtotal = 0
        for i in ordered_products:
            # prod_total = i.product_price * i.quantity
            subtotal += i.product_price * i.quantity


        # payment = Payment.objects.get(payment_id = transID)

        context = {
            # 'prod_total': prod_total,
            'order':order,
            'ordered_products' : ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal':subtotal,
        }
        CartItem.objects.filter(user=request.user).delete()
        return render(request, 'orders/order_complete.html',context)


    except (Payment.DoesNotExist, Order.DoesNotExist):

        print("payment feedback not received. exiting without saving")
        return redirect('home')


