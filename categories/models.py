from django.db import models

from products.models import Product

class Category(models.Model):
    title = models.CharField(max_length=50)
    descriptions = models.TextField()
    products = models.ManyToManyField(Product, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "categoria"
        verbose_name_plural = "categorias"
       
    def __str__(self):
        return self.title 
    