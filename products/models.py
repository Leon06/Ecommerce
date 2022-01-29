
from distutils.command.upload import upload
import uuid
from django.db import models
from django.utils.text import slugify

from django.db.models.signals import pre_save

# Create your models here.

class Product(models.Model):
    title = models.CharField(max_length=50) #max_length  debe conincidir con el numero que hayamos colocado en RegisterForm [forms.py]
    descriptions = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=0, default=0) #1234678.50 decimal_places
    slug = models.SlugField(null=False,blank=False, unique=True)
    image = models.ImageField(upload_to='products/', null=False, blank=False)
    created_at = models.DateField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        
    def __str__(self):
        return self.title
    
    
#generar los slugs
def set_slug(sender, instance, *args, **kwargs): #signal[pre_save]callback
    if instance.title and not instance.slug:
        slug = slugify(instance.title)
        #Generar un slug unico en nuestra BD
        while Product.objects.filter(slug=slug).exists():
            slug = slugify(
                '{}-{}'.format(instance.title, str(uuid.uuid4())[:8])                
            )
        
        instance.slug = slug
    
pre_save.connect(set_slug, sender=Product)