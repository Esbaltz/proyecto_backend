from django.contrib import admin
from .models import Libro, Carrito, CarritoItem

# Register your models here.

admin.site.register(Libro)

class CarritoItemInline(admin.TabularInline):
    model = CarritoItem
    extra = 1

@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    inlines = [CarritoItemInline]
    list_display = ('usuario',)

@admin.register(CarritoItem)
class CarritoItemAdmin(admin.ModelAdmin):
    list_display = ('carrito', 'libro', 'cantidad')
    search_fields = ('carrito__usuario__username', 'libro__titulo')