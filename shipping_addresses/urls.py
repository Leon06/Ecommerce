from django.urls import path
from .views import ShippingAdrressListView, ShippingAddressUpdateView,ShippingAddressDeleteView
from .views import create, default


app_name ='shipping_addresses'

urlpatterns = [
    path('',ShippingAdrressListView.as_view(), name='shipping_addresses'),
    path('nuevo/',create,name='create'),
    path('editar/<int:pk>',ShippingAddressUpdateView.as_view(), name='update'),
    path('eliminar/<int:pk>',ShippingAddressDeleteView.as_view(),name='delete'),
    path('default/<int:pk>',default, name='default')
]
