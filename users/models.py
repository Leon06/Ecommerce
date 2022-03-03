from django.db import models

#from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

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

    


# Generar el proxy models de User
class Customer(User):
    class Meta:
        proxy = True
        

    def get_products(self): #Este metodo va a retornar todos los productos adquiridos por el cliente
        return []

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    