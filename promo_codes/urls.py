from django.urls import path
from .views import validate

app_name= 'promo_code'

urlpatterns = [
    path('validar/',validate,name='validate')
]
