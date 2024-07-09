# Generated by Django 5.0.6 on 2024-06-29 17:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appweb', '0005_alter_libro_tipo'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='libro',
            name='subtipo',
            field=models.CharField(choices=[('Ficción', [('Sci-fi', 'Sci-fi'), ('Misterio', 'Misterio'), ('Terror', 'Terror'), ('Fantasía', 'Fantasia')]), ('No_Ficción', [('Historia', 'Historia'), ('Biografía', 'Biografía')]), ('Sin subtipo', 'Sin Subtipo')], default='Sin subtipo', max_length=40),
        ),
        migrations.CreateModel(
            name='Carrito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CarritoItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField(default=1)),
                ('carrito', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='appweb.carrito')),
                ('libro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appweb.libro')),
            ],
        ),
    ]
