from django.db import models

#from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

#AbstractUser
class User(AbstractUser):
    
   def get_full_name(self):
       return f'{self.first_name} {self.last_name}'

    


# Generar el proxy models de User
class Customer(User):
    class Meta:
        proxy = True
        

    def get_products(self): #Este metodo va a retornar todos los productos adquiridos por el cliente
        return []

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    