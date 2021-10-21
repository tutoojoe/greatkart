from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.decorators import login_required

from store.models import Product,Variation
from carts.models import Cart,CartItem

# Create your views here.

# Private function to check whether there is any session available.
# If not available, create a session, and return the cart to add_cart.
def _cart_id(request):
    cart        = request.session.session_key
    if not cart:
        cart    = request.session.create()
    return cart

def add_cart(request,product_id):
    current_user = request.user
    product     = Product.objects.get(id = product_id)
    # if the user is authenticated
    if current_user.is_authenticated:
        product_variation = []
        # Getting POST request:
        if request.method == 'POST':
            for item in request.POST:
                key     = item
                value   = request.POST[key]
                
                try:
                    variation   = Variation.objects.get(product = product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                    print(variation)
                except:
                    pass
        # Getting a request to add a producct
        # Getting the product
        #product     = Product.objects.get(id = product_id)


        is_cart_item_exists = CartItem.objects.filter(product = product, user=current_user).exists()
        # Adding product at the same time. Checking whether the product is already available in cart.
        # If available, increment the quantity by 1.
        if is_cart_item_exists:
            cart_item           = CartItem.objects.filter(product=product, user=current_user)
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)
            #checke
            if product_variation in ex_var_list:
                print('product already on list. Incrementing the quantity')
                # add the new quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()

            else:
                print('product NOT in list - Adding new item')
                # create a new cart item
                item = CartItem.objects.create(product=product, quantity=1, user=current_user)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                    # adding a star will make surea that the star is whole thing is getting added.
                item.save() 
        # If item does not exist, create the 'cart_item'
        else:
            print('NO CART ITEMS - create a new one')
            cart_item       = CartItem.objects.create(
                product     = product,
                quantity    = 1,
                user        = current_user,
                )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        
        return redirect('cart')


    # if the user is not authenticated
    else:
        product_variation = []
        # Getting POST request:
        if request.method == 'POST':
            for item in request.POST:
                key     = item
                value   = request.POST[key]
                
                try:
                    variation   = Variation.objects.get(product = product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                    print(variation)
                except:
                    pass
        # Getting a request to add a producct
        # Getting the product
        product     = Product.objects.get(id = product_id)
        
        # Checking whether any cart is already open/ available
        # Using a private function(_cart_id), checking the availability of saved session.
        try:
            cart    = Cart.objects.get(cart_id = _cart_id(request))
        # if cart is not available, create the Cart and save.
        except Cart.DoesNotExist:
            cart    = Cart.objects.create(cart_id = _cart_id(request))
            cart.save()

        is_cart_item_exists = CartItem.objects.filter(product = product, cart = cart).exists()
        # Adding product at the same time. Checking whether the product is already available in cart.
        # If available, increment the quantity by 1.
        if is_cart_item_exists:
            cart_item           = CartItem.objects.filter(product=product, cart=cart)
            # we need 
            # existing variations - in database 
            # current variations - new entry
            # item_id
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                # the result of the below will be a queryset. this is converted to list.
                ex_var_list.append(list(existing_variation))
                id.append(item.id)
            
            if product_variation in ex_var_list:
                print('product already on list. Incrementing the quantity')
                # add the new quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()

            else:
                print('product NOT in list - Adding new item')
                # create a new cart item
                item = CartItem.objects.create(product=product, quantity=1, cart=cart)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                    # adding a star will make surea that the star is whole thing is getting added.
                item.save() 
        # If item does not exist, create the 'cart_item'
        else:
            print('NO CART ITEMS - create a new one')
            cart_item       = CartItem.objects.create(
                product     = product,
                quantity    = 1,
                cart        = cart,
                )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        
        return redirect('cart')





 
 # Adding function to remove cart
def remove_cart(request,product_id, cart_item_id):
    
    product     = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item   = CartItem.objects.get(product = product, user=request.user, id=cart_item_id)
        else:
            cart        = Cart.objects.get(cart_id=_cart_id(request))
            cart_item   = CartItem.objects.get(product = product, cart = cart, id=cart_item_id)
        
        if cart_item.quantity >1:
            cart_item.quantity -=1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass    
    return redirect('cart')

# Function to delete the cart item directly with 'Remove' button

def remove_cart_item(request, product_id, cart_item_id):
    
    product     = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item   = CartItem.objects.get(product = product, user = request.user, id=cart_item_id)
    else:
        cart        = Cart.objects.get(cart_id=_cart_id(request))
        cart_item   = CartItem.objects.get(product = product, cart = cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')

# Function to get cart items, total and quantity
def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items  = CartItem.objects.filter(user=request.user, is_active = True)
        else:
            cart        = Cart.objects.get(cart_id = _cart_id(request))
            cart_items  = CartItem.objects.filter(cart = cart, is_active = True).order_by('id')
        for cart_item in cart_items:
            total   += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (5 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass

    context     = {
        'total': total, 
        'quantity': quantity, 
        'cart_items': cart_items,
        'tax':tax,
        'grand_total':grand_total,
        }
    return render(request, 'store/cart.html', context)



@login_required(login_url = 'login')
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items  = CartItem.objects.filter(user=request.user, is_active = True)
            
            for cart_item in cart_items:
                total   += (cart_item.product.price * cart_item.quantity)
                quantity += cart_item.quantity
        tax = (5 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass

    context     = {
        'total': total, 
        'quantity': quantity, 
        'cart_items': cart_items,
        'tax':tax,
        'grand_total':grand_total,
        }


    return render(request,'store/checkout.html',context)