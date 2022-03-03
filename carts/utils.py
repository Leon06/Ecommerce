from .models import Cart

def get_or_create_cart(request):
    
    user = request.user if request.user.is_authenticated else None
    cart_id = request.session.get('cart_id') #Intentamos obtener el cart_id; nos retorna un None si no existe
    cart = Cart.objects.filter(cart_id=cart_id).first()#Intentamos obtener el carrito  #[] -> None
    
    if cart is None:# si el carrito no existe, lo creamos
        cart = Cart.objects.create(user=user)
        
    if user and cart.user is None:#el usuario existe y el carrito no posee un usuario se asigna
        cart.user = user
        cart.save()
        
    request.session['cart_id'] = cart.cart_id #Se actualiza la sesion
    
    return cart

def destroy_cart(request):
    request.session['cart_id'] = None
