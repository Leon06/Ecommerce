
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from django.db.models import Q

from .models import Product

class ProductListView(ListView):
    template_name = 'index.html'
    queryset = Product.objects.all().order_by('-id') #Obtengo los datos de la clase Product [models.py]
    
    #Este metodo se encarga de pasar el contexto de la clasea el template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'Listado de productos'
        
        return context

#DetailView se encargara de obtener un objeto un registro de nuestra base de datos[ el valor del slug lo tomara a traves de la url]
class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product.html'
    
#Buscador de Productos 
class ProductSearchListView(ListView):
    template_name = 'products/search.html'
    
    def get_queryset(self):
        filters = Q(title__icontains= self.query()) | Q(category__title__icontains=self.query())
        #SELECT * FROM products WHERE title like %valor%
        return Product.objects.filter(filters)
    
    def query(self):
        return self.request.GET.get('q')
    
    #Resultados para [lo que el usuario coloque en el input]
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.query()
        context['count'] = context['product_list'].count()
        
        return context
    
    