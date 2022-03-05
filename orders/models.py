import decimal
from enum import Enum

import uuid
from django.db import models
from promo_codes.models import PromoCode
from shipping_addresses.models import ShippingAddress
from users.models import User
from carts.models import Cart

from django.db.models.signals import pre_save

from .common import OrderStatus
from .common import choices

from promo_codes.models import PromoCode



class Order(models.Model):
    order_id = models.CharField(max_length=100,null=False,unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=50,choices=choices, default=OrderStatus.CREATED)
    shipping_total = models.DecimalField(default=0, max_digits=8,decimal_places=0)
    total = models.DecimalField(default=0, max_digits=8,decimal_places=0)
    created_at= models.DateTimeField(auto_now_add=True)
    shipping_address = models.ForeignKey(ShippingAddress, null=True, blank=True, on_delete=models.CASCADE)
    promo_code = models.OneToOneField(PromoCode, null=True, blank=True, on_delete=models.CASCADE)


    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "pedidos"

    def __str__(self):
        return self.order_id

    #PomoCode
    def apply_promo_code(self, promo_code):
        if self.promo_code is None:
            self.promo_code = promo_code
            self.save()

            self.update_total()
            promo_code.use()

    
    def update_total(self):
        self.total = self.get_total()
        self.save()


    def get_discount(self):
        if self.promo_code:
            return self.promo_code.discount

        return 0

    def get_total(self):
        return self.cart.total + self.shipping_total - decimal.Decimal(self.get_discount())

    #Establecemos la direccion de envio a nuestra orden
    def get_or_set_shipping_address(self):
        if self.shipping_address:
            return self.shipping_address
        
        shipping_address = self.user.shipping_address#Obtenemos la direccion principal del usuario
        if shipping_address:
            self.update_shipping_address(shipping_address)

        return shipping_address

    def update_shipping_address(self, shipping_address):
        self.shipping_address = shipping_address
        self.save()

    def cancel(self):
        self.status = OrderStatus.CANCELED
        self.save()

    def complete(self):
        self.status =OrderStatus.COMPLETED
        self.save()


        
#callback (signals)
def set_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = str(uuid.uuid4())

def set_total(sender, instance, *args, **kwargs):
    instance.total = instance.get_total()

pre_save.connect(set_order_id, sender=Order)
pre_save.connect(set_total, sender=Order)