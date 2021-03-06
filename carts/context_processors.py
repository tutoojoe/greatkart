from carts.models import CartItem,Cart, WishCart, Wishlist
from .views import _cart_id, _wishcart_id



def counter(request):
    cart_count = 0

    if 'admin' in request.path:
        return {}
    else:
        try:
            cart        = Cart.objects.filter(cart_id = _cart_id(request))
            if request.user.is_authenticated:
                cart_items   = CartItem.objects.all().filter(user = request.user)
            else:
                cart_items   = CartItem.objects.all().filter(cart = cart [:1])
            # above query will return only one result

            # Now getting the quantity from cart_item (as the quantity is mentioned in the model)
            for cart_item in cart_items:
                cart_count += cart_item.quantity
        except Cart.DoesNotExist:
            cart_count = 0
    return dict(cart_count=cart_count)


def wish_list(request):
    if request.user.is_authenticated:
        wish_items = Wishlist.objects.filter(user = request.user).count()
        return{'wish_items': wish_items}
    else:
        return{'wish_items': 0}
