from django.shortcuts import render
from django.views.generic import ListView

from .models import ShippingAddress
from .forms import ShippingAddresForm
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required #permite restringir el acceso a vistas de usuarios no autenticados
from django.contrib.auth.mixins import LoginRequiredMixin


class ShippingAdrressListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = ShippingAddress
    template_name = "shipping_addresses/shipping_addresses.html"

    def get_queryset(self):
        return ShippingAddress.objects.filter(user=self.request.user).order_by('-default')

@login_required(login_url='login')
def create(request):
    form = ShippingAddresForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        shipping_address = form.save(commit=False)
        shipping_address.user = request.user
        shipping_address.default = not ShippingAddress.objects.filter(user=request.user).exists()

        shipping_address.save()

        messages.success(request, 'Dirección creada correctamente')
        return redirect('shipping_addresses:shipping_addresses')

    return render(request, 'shipping_addresses/create.html',{'form':form})
    