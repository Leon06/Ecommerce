
from itertools import product
from django.shortcuts import render
from django.shortcuts import redirect

from django.contrib import messages
from django.contrib.auth import login 
from django.contrib.auth import logout
from django.contrib.auth import authenticate

#from django.contrib.auth.models import User
from users.models import User

from products.models import Product 

from .forms import RegisterForm





# Autenticar Usuario LOGIN
def login_view(request):
    
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        username = request.POST.get('username') #diccionario
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Bienvenido {user.username}')           
            return redirect('index')
        else:
            messages.error(request, 'Usuario no valido')
            
    return render(request,'users/login.html',{
        
    })
    
# Salir  
def logout_view(request):
    logout(request)
    messages.success(request, 'Sesión cerrada exitosamente')
    return redirect('login')

# Registrar Usuario [basado en clases]   
def register(request):
    #Verifico si el usuario esta registrado y lo redirecciono [index]
    if request.user.is_authenticated:
        return redirect('index')
    
    form = RegisterForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid(): 
        #cree la funcion [save] en forms.py       
        user = form.save()
        if user:
            login(request, user)
            messages.success(request, 'Usuario creado exitosamente')
            return redirect('index')
        
    return render(request,'users/register.html',{
        
        'form': form
        
    })
    