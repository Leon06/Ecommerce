from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from carts.views import cart
from orders.mails import Mail
from shipping_addresses.models import ShippingAddress

from .utils import breadcrumb
from .utils import get_or_created_order
from .utils import destroy_order


from carts.models import Cart
from carts.utils import get_or_create_cart
from carts.utils import destroy_cart

@login_required(login_url='login')
def order(request):
    cart = get_or_create_cart(request)
    order = get_or_created_order(cart, request)

    return render(request, 'orders/order.html',{
        'cart':cart,
        'order':order,
        'breadcrumb' : breadcrumb()

    })

@login_required(login_url='login')
def address(request):
    cart = get_or_create_cart(request)
    order = get_or_created_order(cart,request)

    shipping_address = order.get_or_set_shipping_address #Asi obtenemos la direccion de envio de la orden
    can_choose_address = request.user.shippingaddress_set.count()>1

    return render(request,'orders/address.html',{
        'cart': cart,
        'order': order,
        'shipping_address': shipping_address,
        'breadcrumb': breadcrumb(),
        'can_choose_address':can_choose_address
    })

@login_required(login_url='login')
def select_address(request):
    shipping_addresses = request.user.shippingaddress_set.all()#obtenemos todas las direcciones del usuario autenticado

    return render(request, 'orders/select_address.html',{
        'breadcrumb':breadcrumb(address=True),
        'shipping_addresses':shipping_addresses
    })

@login_required(login_url='login')
def check_address(request,pk):
    cart = get_or_create_cart(request)
    order = get_or_created_order(cart, request) #obtenemos la orden de compra

    shipping_address = get_object_or_404(ShippingAddress, pk=pk)

    if request.user.id != shipping_address.user_id:#validamos  que sea el usuario quien creo la direccion el que pueda utilizarla
        return redirect('carts:cart')

    order.update_shipping_address(shipping_address)
    return redirect('orders:address')


@login_required(login_url='login')
def confirm(request):
    cart= get_or_create_cart(request)
    order = get_or_created_order(cart, request)

    shipping_address = order.shipping_address
    if shipping_address is None:
        return redirect('orders:address')

    return render(request,'orders/confirm.html',{

        'cart':cart,
        'order':order,
        'shipping_address':shipping_address,
        'breadcrumb': breadcrumb(address=True, confirmation=True)
    })


@login_required(login_url='login')
def cancel(request):
    cart = get_or_create_cart(request)
    order = get_or_created_order(cart, request)

    if request.user.id != order.user_id:
        return redirect('carts:cart')

    order.cancel()
    destroy_cart(request)
    destroy_order(request)

    messages.error(request, 'Orden cancelada')
    return redirect('index')


@login_required(login_url='login')
def complete(request):

    cart =get_or_create_cart(request)
    order = get_or_created_order(cart,request)

    if request.user.id != order.user_id:
        return redirect('carts:cart')

    order.complete()
    Mail.send_complete_order(order,request.user)

    destroy_cart(request)
    destroy_order(request)

    messages.success(request, 'Compra completada exitosamente')
    return redirect('index')




