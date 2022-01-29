from itertools import product
from django.shortcuts import get_object_or_404, redirect, render
from .models import Cart
from .utils  import get_or_create_cart
from django.shortcuts import redirect
from products.models import Product
from django.shortcuts import get_object_or_404

def cart(request):
    cart = get_or_create_cart(request)# Obtenemos el carro de compras    
    return render(request, "carts/cart.html",{
        'cart': cart
    })

def add(request):
    cart = get_or_create_cart(request) 
    product = get_object_or_404(Product, pk=request.POST.get('product_id'))
    #product = Product.objects.get(pk=request.POST.get('product_id'))# Obtenemnos el producto del formulario add.html
    quantity = request.POST.get('quantity', 1) #Obtenemos la llave del input en snippets/add.html , valor por default 1
    
    cart.products.add(product, through_defaults = { #Agregar productos al carrito de compras(tienen relacion manytomany)
        'quantity' : quantity
        }) 
    
    return render(request,'carts/add.html',{
        'product': product
    })
 

def remove(request):  
    cart = get_or_create_cart(request) 
    product = get_object_or_404(Product, pk=request.POST.get('product_id'))
    
    cart.products.remove(product)
    
    return redirect('carts:cart')