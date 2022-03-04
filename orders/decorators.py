#Decoradores para app order

from carts.utils import get_or_create_cart
from .utils import get_or_created_order

def validate_cart_and_order(function):
    def wrap(request,*args, **kwargs):
        cart = get_or_create_cart(request)#Obtener el carrito
        order = get_or_created_order(cart, request)#Obtener la orden
        return function(request, cart, order, *args, **kwargs)

    return wrap

 

    



