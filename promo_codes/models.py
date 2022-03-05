
from django.db import models
from django.db.models.signals import pre_save
import string
import random

class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.FloatField(default=0.0)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.code

    class Meta:
        verbose_name = "Código promocional"
        verbose_name_plural = "Códigos promocionales"

    def use(self):
        self.used = True
        self.save()


#callback(signal)
def set_code (sender, instance, *args, **kwargs):
    if instance.code:
        return

    chars= string.ascii_uppercase + string.digits
    instance.code = ''.join(random.choice(chars) for _ in range(10))


#Antes de que un obj de la clase PromoCode ejecute el metodo save ...va a ejecutarse el metodo callback set_code
pre_save.connect(set_code, sender=PromoCode)