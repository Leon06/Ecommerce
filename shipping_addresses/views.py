
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView
from django.views.generic.edit import UpdateView, DeleteView

from carts.models import Cart
from carts.utils import get_or_create_cart
from orders.utils import get_or_created_order

from .models import ShippingAddress
from .forms import ShippingAddresForm
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required #permite restringir el acceso a vistas de usuarios no autenticados
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin


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
        shipping_address.default = not request.user.has_shipping_address()

        shipping_address.save()

        if request.GET.get('next'):
            if request.GET['next'] == reverse ('orders:address'):
                cart = get_or_create_cart(request)
                order = get_or_created_order(cart, request)

                order.update_shipping_address(shipping_address)

                return HttpResponseRedirect(request.GET['next'])

        messages.success(request, 'Dirección creada correctamente')
        return redirect('shipping_addresses:shipping_addresses')

    return render(request, 'shipping_addresses/create.html',{'form':form})
    
class ShippingAddressUpdateView(LoginRequiredMixin,SuccessMessageMixin,UpdateView ):        

    login_url = 'login'  #LoginRequiredMixin
    model = ShippingAddress
    form_class = ShippingAddresForm
    template_name = 'shipping_addresses/update.html'
    success_message = 'Dirección actualizada exitosamente'

    def get_success_url(self):
        return reverse('shipping_addresses:shipping_addresses')

    def dispatch(self,request, *args, **kwargs): #Metodo nos permite implementar validaciones sobre la peticion
        if request.user.id != self.get_object().user.id:
            return redirect('carts:cart')

        return super(ShippingAddressUpdateView, self).dispatch(request, *args, **kwargs)


class ShippingAddressDeleteView(LoginRequiredMixin, DeleteView):
    login_url ='login' #LoginRequiredMixin
    model = ShippingAddress
    template_name = 'shipping_addresses/delete.html'
    success_url = reverse_lazy ('shipping_addresses:shipping_addresses') 

    def dispatch(self,request, *args, **kwargs): #Metodo nos permite implementar validaciones sobre la peticion
        if self.get_object().default:
            return redirect('shipping_addresses:shipping_addresses')
        
        if request.user.id != self.get_object().user.id:
            return redirect('carts:cart') 
        

        if self.get_object().has_orders(): # El objeto de ShippingAddress no puede ser eliminado si este tiene relacion con una orden
            return redirect('shipping_addresses:shipping_addresses')


        return super(ShippingAddressDeleteView, self).dispatch(request, *args, **kwargs)


@login_required(login_url='login')
def default(request,pk):
    shipping_address = get_object_or_404(ShippingAddress, pk=pk)

    if request.user.id != shipping_address.user_id:
        return redirect('carts:cart')

    if request.user.has_shipping_address():
        #Obtener la antigua direccion principal y colocar default como False
        request.user.shipping_address.update_default()
        
    shipping_address.update_default(True)

    return redirect('shipping_addresses:shipping_addresses')
