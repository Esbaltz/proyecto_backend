from django.shortcuts import render, get_object_or_404, redirect
from .forms import LibroForm, LibroFormMod, LoginForm, ItemForm, CustomUserChangeForm 
from .models import Libro, Carrito, CarritoItem, Compra, CompraItem
import random
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    # Obtener todos los libros
    todos_libros = Libro.objects.all()

    # Obtener 4 libros aleatorios de todos los libros
    if todos_libros.count() >=4:
        libros_req = random.sample(list(todos_libros), 4)
    else:
        libros_req = list(todos_libros)
    # Obtener solo los libros que son best sellers
    libros_best_sellers = todos_libros.filter(best_seler=True)

    # Verificar si hay al menos 4 libros best sellers disponibles
    if libros_best_sellers.count() >= 4:
        libros_aleatorios = list(libros_best_sellers.order_by('?')[:4])
    else:
        libros_aleatorios = list(libros_best_sellers)

    context = {
        'libros_aleatorios': libros_aleatorios,
        'libros_req': libros_req,  # Pasar los libros aleatorios de todos los libros a la plantilla
    }

    return render(request, 'index.html', context)

def tienda(request):
    todos_libros = Libro.objects.all()

    # Obtener 4 libros aleatorios de todos los libros
    if todos_libros.count() >=4:
        libros_req = random.sample(list(todos_libros), 4)
    else:
        libros_req = list(todos_libros)
    # Obtener solo los libros que son best sellers
    libros_best_sellers = todos_libros.filter(best_seler=True)

    # Verificar si hay al menos 4 libros best sellers disponibles
    if libros_best_sellers.count() >= 4:
        libros_aleatorios = list(libros_best_sellers.order_by('?')[:4])
    else:
        libros_aleatorios = list(libros_best_sellers)

    context = {
        'libros_aleatorios': libros_aleatorios,
        'libros_req': libros_req,  # Pasar los libros aleatorios de todos los libros a la plantilla
    }
    return render(request, 'tienda.html', context)

@login_required
def user(request):
    # Obtener el usuario actual
    usuario_actual = request.user
    
    # Filtrar las compras del usuario actual ordenadas por fecha descendente
    compras = Compra.objects.filter(usuario=usuario_actual).order_by('-fecha')
    
    # Obtener los ítems de compra relacionados con las compras filtradas
    items_por_compra = {compra: CompraItem.objects.filter(compra=compra) for compra in compras}

    return render(request, 'user.html', {
        'compras': compras,
        'items_por_compra': items_por_compra,
    })

def permiso(request):
    return render(request, 'permiso.html')
    
@permission_required('appweb.delete_libro')
def agregar(request):
    exito = False  # Variable para controlar si mostrar el mensaje de éxito
    
    if request.method == 'POST':
        form = LibroForm(request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            exito = True  # Cambia el estado de éxito a True después de guardar el libro correctamente
    else:
        form = LibroForm()

    data = {
        'form': form,
        'exito': exito,  # Pasar la variable exito al contexto de la plantilla
    }
    return render(request, 'admin/agregar.html', data)

@permission_required('appweb.delete_libro')
def listar(request):
    libros = Libro.objects.all()

    data={
        'libros': libros
    }
    return render(request, 'admin/listar.html', data)

@permission_required('appweb.delete_libro')
def modificar(request, isbn):
    libro = get_object_or_404(Libro, isbn=isbn)
    exito = False

    if request.method == 'POST':
        formulario = LibroFormMod(request.POST, request.FILES, instance=libro)
        if formulario.is_valid():
            formulario.save()
            exito = True  # Cambia el estado de éxito a True después de guardar los cambios correctamente
    else:
        formulario = LibroFormMod(instance=libro)
        # No permitir modificar el campo isbn en el formulario
        formulario.fields['isbn'].disabled = True

    data = {
        'form': formulario,
        'exito': exito,  # Pasar la variable exito al contexto de la plantilla
    }
    return render(request, 'admin/modificar.html', data)

@permission_required('appweb.delete_libro')
def eliminar(request, isbn):
    libro = get_object_or_404(Libro, isbn=isbn)
    libro.delete()
    return redirect(to="listar")

def detalle_libro(request, isbn):
    # Obtener el libro específico por su ISBN
    libro = get_object_or_404(Libro, isbn=isbn)

    libros_rec = Libro.objects.all()
    todos_libros = Libro.objects.all()
    if todos_libros.count() >=4:
        libros_req = random.sample(list(todos_libros), 4)
    else:
        libros_req = list(todos_libros)

    context = {
        'libro': libro,
        'libros_r': libros_req,
    }
    
    return render(request, 'detalle_libro.html', context)

def sci_fi(request):
    # Filtrar libros de ciencia ficción
    libros = Libro.objects.filter(tipo='Ficción', subtipo='Sci-fi')
    libros_best_sellers = libros.filter(best_seler=True)

    # Obtener 4 libros aleatorios de ciencia ficción
    if libros.count() >= 4:
        libros_req = list(libros.order_by('?')[:4])
    else:
        libros_req = list(libros)

    # Obtener 4 best sellers aleatorios de ciencia ficción
    if libros_best_sellers.count() >= 4:
        libros_rec = list(libros_best_sellers.order_by('?')[:4])
    else:
        libros_rec = list(libros_best_sellers)

    context = {
        'libros_req': libros_req,
        'libros_rec': libros_rec,
    }
    return render(request, 'sci_fi.html', context)

def terror(request):
    libros = Libro.objects.filter(tipo='Ficción', subtipo='Terror')
    libros_best_sellers = libros.filter(best_seler=True)

    # Obtener 4 libros aleatorios de ciencia ficción
    if libros.count() >= 4:
        libros_req = list(libros.order_by('?')[:4])
    else:
        libros_req = list(libros)

    # Obtener 4 best sellers aleatorios de ciencia ficción
    if libros_best_sellers.count() >= 4:
        libros_rec = list(libros_best_sellers.order_by('?')[:4])
    else:
        libros_rec = list(libros_best_sellers)

    context = {
        'libros_req': libros_req,
        'libros_rec': libros_rec,
    }
    return render(request, 'terror.html', context)

def misterio(request):
    libros = Libro.objects.filter(tipo='Ficción', subtipo='Misterio')
    libros_best_sellers = libros.filter(best_seler=True)

    # Obtener 4 libros aleatorios de ciencia ficción
    if libros.count() >= 4:
        libros_req = list(libros.order_by('?')[:4])
    else:
        libros_req = list(libros)

    # Obtener 4 best sellers aleatorios de ciencia ficción
    if libros_best_sellers.count() >= 4:
        libros_rec = list(libros_best_sellers.order_by('?')[:4])
    else:
        libros_rec = list(libros_best_sellers)

    context = {
        'libros_req': libros_req,
        'libros_rec': libros_rec,
    }
    return render(request, 'misterio.html', context)

def historia(request):
    # Filtrar libros de historia dentro de la categoría "No_Ficción"
    libros = Libro.objects.filter(tipo='No_Ficción', subtipo='Historia')
    libros_best_sellers = libros.filter(best_seler=True)

    # Obtener 4 libros aleatorios de historia
    if libros.count() >= 4:
        libros_req = list(libros.order_by('?')[:4])
    else:
        libros_req = list(libros)

    # Obtener 4 best sellers aleatorios de historia
    if libros_best_sellers.count() >= 4:
        libros_rec = list(libros_best_sellers.order_by('?')[:4])
    else:
        libros_rec = list(libros_best_sellers)

    context = {
        'libros_req': libros_req,
        'libros_rec': libros_rec,
    }
    return render(request, 'historia.html', context)

def fantasia(request):
    # Obtener todos los libros de la categoría "Fantasía"
    libros = Libro.objects.filter(tipo='Ficción', subtipo='Fantasía')
    libros_r = Libro.objects.filter(tipo='Ficción', subtipo='Fantasía', best_seler=True)

    # Obtener 4 libros aleatorios de la categoría "Fantasía"
    if libros.count() >= 4:
        libros_req = list(libros.order_by('?')[:4])
    else:
        libros_req = list(libros)

    if libros_r.count() >= 4:
        libros_rec = list(libros_r.order_by('?')[:4])
    else:
        libros_rec = list(libros_r)

    context = {
        'libros_req': libros_req,
        'libros_rec': libros_rec,
    }

    return render(request, 'fantasia.html', context)

def biografia(request):
    # Filtrar libros de biografía dentro de la categoría "No_Ficción"
    libros = Libro.objects.filter(tipo='No_Ficción', subtipo='Biografía')
    libros_best_sellers = libros.filter(best_seler=True)

    # Obtener 4 libros aleatorios de biografía
    if libros.count() >= 4:
        libros_req = list(libros.order_by('?')[:4])
    else:
        libros_req = list(libros)

    # Obtener 4 best sellers aleatorios de biografía
    if libros_best_sellers.count() >= 4:
        libros_rec = list(libros_best_sellers.order_by('?')[:4])
    else:
        libros_rec = list(libros_best_sellers)

    context = {
        'libros_req': libros_req,
        'libros_rec': libros_rec,
    }
    return render(request, 'biografia.html', context)

@login_required
def pagar(request):
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    libros_en_carrito = CarritoItem.objects.filter(carrito=carrito)

    if not libros_en_carrito.exists():
        return redirect('carrito')

    compra = Compra.objects.create(usuario=request.user)
    for item in libros_en_carrito:
        CompraItem.objects.create(compra=compra, libro=item.libro, cantidad=item.cantidad)
        item.delete()

    return redirect('user')  # Redirige a una página de confirmación de compra

@login_required
def carrito(request):
    if request.user.is_authenticated:
        carrito, created = Carrito.objects.get_or_create(usuario=request.user)
        libros_en_carrito = CarritoItem.objects.filter(carrito=carrito)
        total = sum(item.libro.precio * item.cantidad for item in libros_en_carrito)

        return render(request, 'carrito.html', {
            'libros_en_carrito': libros_en_carrito,
            'total': total,
        })
    else:
        return redirect('sesion')

def agregar_carrito(request, isbn):
    libro = get_object_or_404(Libro, isbn=isbn)
    if request.user.is_authenticated:
        carrito, created = Carrito.objects.get_or_create(usuario=request.user)
        item, item_created = CarritoItem.objects.get_or_create(carrito=carrito, libro=libro)
        if not item_created:
            item.cantidad += 1
        item.save()

        return redirect('detalle_libro', isbn=isbn)
    else:
        return redirect('sesion')

def eliminar_carrito(request, isbn):
    libro = get_object_or_404(Libro, isbn=isbn)
    if request.user.is_authenticated:
        carrito = get_object_or_404(Carrito, usuario=request.user)
        item = get_object_or_404(CarritoItem, carrito=carrito, libro=libro)
        item.delete()

        return redirect('carrito')
    else:
        return redirect('sesion')

def vaciar_carrito(request):
    if request.user.is_authenticated:
        carrito = get_object_or_404(Carrito, usuario=request.user)
        CarritoItem.objects.filter(carrito=carrito).delete()

        return redirect('carrito')
    else:
        return redirect('sesion')
    
def aumentar_cantidad(request, isbn):
    if request.user.is_authenticated:
        carrito, created = Carrito.objects.get_or_create(usuario=request.user)
        item = get_object_or_404(CarritoItem, carrito=carrito, libro__isbn=isbn)
        item.cantidad += 1
        item.save()
    return redirect('carrito')

def disminuir_cantidad(request, isbn):
    if request.user.is_authenticated:
        carrito, created = Carrito.objects.get_or_create(usuario=request.user)
        item = get_object_or_404(CarritoItem, carrito=carrito, libro__isbn=isbn)
        if item.cantidad > 1:
            item.cantidad -= 1
            item.save()
    return redirect('carrito')

def sesion(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirigir a una página después del inicio de sesión exitoso
                return redirect('index')  # Ajusta 'index' según tu configuración de URLs
            else:
                messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
    else:
        form = LoginForm()

    return render(request, 'sesion.html', {'form': form})

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'¡Cuenta creada para {username}!')
            return redirect('sesion')
    else:
        form = UserCreationForm()
    return render(request, 'registro.html', {'form': form})

def salir(request):
    logout(request)
    messages.info(request,'Sesión Cerrada')
    return redirect(to="index")

@login_required
def pedidos(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        item = get_object_or_404(CompraItem, id=item_id)
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('pedidos')
    else:
        form = ItemForm()

    compras = Compra.objects.all().order_by('-fecha')
    items_por_compra = {compra: CompraItem.objects.filter(compra=compra) for compra in compras}

    return render(request, 'admin/pedidos.html', {
        'compras': compras,
        'items_por_compra': items_por_compra,
        'form': form,
    })
    
@permission_required('appweb.delete_libro')
def cuentas(request):
    usuarios = User.objects.exclude(username='admin')

    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')
        usuario = User.objects.get(id=usuario_id)
        usuario.delete()
        return redirect('cuentas')  # Redirige de vuelta a la misma página después de eliminar
    
    return render(request, 'admin/cuentas.html', {'usuarios': usuarios})
@permission_required('appweb.delete_libro')
def modificar_cuenta(request, usuario_id):
    usuario = User.objects.get(id=usuario_id)
    
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, f'Se ha modificado la cuenta de {usuario.username}.')
            return redirect('cuentas')  # Redirige a la lista de cuentas después de modificar
    else:
        form = CustomUserChangeForm(instance=usuario)
    
    return render(request, 'admin/modificar_cuenta.html', {'form': form, 'usuario': usuario})