from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
#from .models import Product
from django import forms
from .models import Libro, CompraItem
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(label="Nombre de usuario")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'password', 'is_superuser')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar etiquetas de campos si es necesario
        self.fields['username'].label = 'Nombre de usuario'
        self.fields['password'].help_text = 'Deje este campo en blanco si no desea cambiar la contraseña.'
        self.fields['is_superuser'].label = 'Es superusuario'

class ItemForm(forms.ModelForm):
    class Meta:
        model = CompraItem
        fields = ['estado']
    
    
class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['isbn', 'nombre', 'nombre_autor', 'foto', 'precio', 'best_seler', 'tipo', 'subtipo']

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if len(nombre) < 3:
            raise forms.ValidationError('El nombre del libro debe tener al menos 3 caracteres.')
        return nombre

    def clean_isbn(self):
        isbn = self.cleaned_data.get('isbn')
        if len(isbn) < 10 or len(isbn) > 13:
            raise forms.ValidationError('El ISBN debe tener entre 10 y 13 caracteres.')
        return isbn

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio < 0:
            raise forms.ValidationError('El precio no puede ser negativo.')
        return precio

    def clean_nombre_autor(self):
        nombre_autor = self.cleaned_data.get('nombre_autor')
        if len(nombre_autor) < 3:
            raise forms.ValidationError('El nombre del autor debe se mayor a 3 cáracteres.')
        # Aquí podrías agregar otras validaciones según tus requisitos
        return nombre_autor

    # Añade más métodos clean_ según sea necesario para otros campos

    def clean_foto(self):
        foto = self.cleaned_data.get('foto')
        # Puedes agregar validaciones personalizadas para la foto si lo necesitas
        return foto

    def clean_best_seler(self):
        best_seler = self.cleaned_data.get('best_seler')
        # Puedes agregar validaciones personalizadas para best_seler si lo necesitas
        return best_seler

    def clean_tipo(self):
        tipo = self.cleaned_data.get('tipo')
        # Puedes agregar validaciones personalizadas para tipo si lo necesitas
        return tipo

    def clean_subtipo(self):
        subtipo = self.cleaned_data.get('subtipo')
        # Puedes agregar validaciones personalizadas para subtipo si lo necesitas
        return subtipo
    
class LibroFormMod(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['isbn', 'nombre', 'nombre_autor', 'foto', 'precio', 'best_seler', 'tipo', 'subtipo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Deshabilitar el campo isbn y establecer su valor si existe una instancia
        self.fields['isbn'].disabled = True
        if kwargs.get('instance'):
            self.initial['isbn'] = kwargs['instance'].isbn

    def clean_isbn(self):
        # Validar que el isbn no cambie, aunque el campo esté presente
        return self.instance.isbn if self.instance else self.cleaned_data.get('isbn')

    def save(self, commit=True):
        # Sobreescribir el método save para evitar cambios en el ISBN
        if not self.instance.pk:  # Nuevo objeto, no hay que hacer nada especial
            return super().save(commit=commit)

        # Actualizar el objeto existente sin cambiar el ISBN
        instance = super().save(commit=False)
        instance.isbn = self.instance.isbn  # Mantener el mismo ISBN
        if commit:
            instance.save()
        return instance

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if len(nombre) < 3:
            raise forms.ValidationError('El nombre del libro debe tener al menos 3 caracteres.')
        return nombre

    def clean_isbn(self):
        isbn = self.cleaned_data.get('isbn')
        if len(isbn) < 10 or len(isbn) > 13:
            raise forms.ValidationError('El ISBN debe tener entre 10 y 13 caracteres.')
        return isbn

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio < 0:
            raise forms.ValidationError('El precio no puede ser negativo.')
        return precio

    def clean_nombre_autor(self):
        nombre_autor = self.cleaned_data.get('nombre_autor')
        if len(nombre_autor) < 3:
            raise forms.ValidationError('El nombre del autor debe se mayor a 3 cáracteres.')
        # Aquí podrías agregar otras validaciones según tus requisitos
        return nombre_autor

    # Añade más métodos clean_ según sea necesario para otros campos

    def clean_foto(self):
        foto = self.cleaned_data.get('foto')
        # Puedes agregar validaciones personalizadas para la foto si lo necesitas
        return foto

    def clean_best_seler(self):
        best_seler = self.cleaned_data.get('best_seler')
        # Puedes agregar validaciones personalizadas para best_seler si lo necesitas
        return best_seler

    def clean_tipo(self):
        tipo = self.cleaned_data.get('tipo')
        # Puedes agregar validaciones personalizadas para tipo si lo necesitas
        return tipo

    def clean_subtipo(self):
        subtipo = self.cleaned_data.get('subtipo')
        # Puedes agregar validaciones personalizadas para subtipo si lo necesitas
        return subtipo