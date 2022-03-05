from django.db import models

#from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from orders.common import OrderStatus

#AbstractUser
class User(AbstractUser):
    
    def get_full_name(self):
       return f'{self.first_name} {self.last_name}'

    @property
    def shipping_address(self):
        return self.shippingaddress_set.filter(default=True).first()

    #Con este metodo vamos a conocer si el usuario posee o No una direccion principal
    def has_shipping_address(self):
        return self.shipping_address is not None

    def orders_completed(self):
        return self.order_set.filter(status=OrderStatus.COMPLETED).order_by('-id')#queryset

    #Nos permitira conocer si el usuario posee direcciones
    def has_shipping_addresses(self):
        return self.shippingaddress_set.exists()

    #obtenemos todas las direcciones del usuario autenticado
    @property
    def addresses(self):
        return self.shippingaddress_set.all()


# Generar el proxy models de User
class Customer(User):
    class Meta:
        proxy = True
        

    def get_products(self): #Este metodo va a retornar todos los productos adquiridos por el cliente
        return []

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    