from django.urls import path
from .views import ShippingAdrressListView
from .views import create


app_name ='shipping_addresses'

urlpatterns = [
    path('',ShippingAdrressListView.as_view(), name='shipping_addresses'),
    path('nuevo/',create,name='create')
]
