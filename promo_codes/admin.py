from django.contrib import admin
from .models import PromoCode


class PromoCodeAdmin(admin.ModelAdmin):
    exclude = ['code']#Quitamos el campo code en el administrador

admin.site.register(PromoCode,PromoCodeAdmin)
