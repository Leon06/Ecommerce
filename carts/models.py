import decimal
from itertools import product
from django.db import models

import uuid

from django.forms import model_to_dict

from users.models import User
from products.models import Product
#Signals
from django.db.models.signals import pre_save
from django.db.models.signals import m2m_changed

class Cart(models.Model):
    cart_id= models.CharField(max_length=100, null=False, blank=False, unique=True)
    user = models.ForeignKey(User,null=True, blank=True, on_delete=models.CASCADE) #uno a muchos
    products = models.ManyToManyField(Product, through='CartProducts') #Muchos a muchos
    subtotal = models.DecimalField(default=0, max_digits=8, decimal_places=0)
    total = models.DecimalField(default=0, max_digits=8, decimal_places=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    FEE = 0.02 #0.2%
    
    def __str__(self):
        return self.cart_id
    
    def update_totals(self):
        self.update_subtotal()
        self.update_total()
        
    def update_subtotal(self):
        self.subtotal = sum([ product.price for product in self.products.all()])
        self.save()
    
    def update_total(self):
        self.total = self.subtotal + (self.subtotal * decimal.Decimal(Cart.FEE))
        self.save()
  
    # Obtenemos todos los objetos CartProducts y a su vez todos los objetos Product
    def products_related(self):
      return self.cartproducts_set.select_related('product')
  
  
  
# Relacion entre un carrito y un producto
class CartProducts(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
def set_cart_id(sender, instance, *args, **kwargs):
    if not instance.cart_id:
        instance.cart_id = str(uuid.uuid4())
        

def update_totals(sender,instance,action, *args, **kwargs):
    if action == 'post_add' or action== 'post_remove' or action=='post_clear':
        instance.update_totals()


pre_save.connect(set_cart_id, sender=Cart)
m2m_changed.connect(update_totals, sender=Cart.products.through)