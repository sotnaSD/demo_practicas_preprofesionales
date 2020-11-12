# Generated by Django 3.1.2 on 2020-11-11 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProductoMercadoLibre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_busqueda', models.IntegerField()),
                ('id_producto', models.IntegerField()),
                ('titulo', models.CharField(max_length=200)),
                ('precio', models.CharField(max_length=30)),
                ('ubicacion', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=500)),
                ('url', models.CharField(max_length=200)),
            ],
        ),
    ]
