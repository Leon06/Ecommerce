from enum import Enum
from django.db import models
from users.models import User
from carts.models import Cart

class OrderStatus(Enum):
    CREATED = 'CREATED'
    PAYED = 'PAYED'
    COMPLETED = 'COMPLETED'
    CANCELED = 'CANCELED'

choices = [(tag, tag.value) for tag in OrderStatus]


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=50,choices=choices, default=OrderStatus.CREATED)

    shipping_total = models.DecimalField(default=5, max_digits=8,decimal_places=2)
    total = models.DecimalField(default=0, max_digits=8,decimal_places=2)
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return ''