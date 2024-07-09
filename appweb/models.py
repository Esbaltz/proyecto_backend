from django.db import models
from .listas import TIPO_GENERO,SUBTIPO_GENERO, ESTADO
from django.core.validators import MinValueValidator
from django.db import models
from django import forms
from django.contrib.auth.models import User

# Create your models here.
class Libro(models.Model):
    #no se si dejar el isbn como clave primaria o ponerle un id para diferenciarlos
    isbn=models.CharField(max_length=13, primary_key=True, null=False)
    nombre=models.CharField(max_length=50, null=False)
    nombre_autor=models.CharField(max_length=50, null=False, default='no posee autor')#falta el autor en el html
    foto=models.ImageField("Imagen",upload_to='libros',null=True)
    precio=models.IntegerField(validators=[MinValueValidator(0)])
    best_seler= models.BooleanField(default=False)#Falta agregar en el html el boton deslizante de si o no en el html

    tipo=models.CharField(max_length=30, choices=TIPO_GENERO, default='Sin tipo')
    subtipo=models.CharField(max_length=40, choices=SUBTIPO_GENERO, default='Sin subtipo')
    def __str__(self):
        return self.nombre
        #return f"nombre {self.nombre} precio: {self.precio} "

class LoginForm(forms.Form):
    username = forms.CharField(label="Nombre de usuario")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)

class Carrito(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

class CarritoItem(models.Model):
    carrito = models.ForeignKey(Carrito, related_name='items', on_delete=models.CASCADE)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

class Compra(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)

class CompraItem(models.Model):
    compra = models.ForeignKey(Compra, related_name='items', on_delete=models.CASCADE)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    estado=models.CharField(max_length=40, choices=ESTADO)

    def __str__(self):
        return self.libro