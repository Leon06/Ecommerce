# Generated by Django 2.2.3 on 2022-01-28 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20220125_2111'),
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='products',
            field=models.ManyToManyField(through='carts.CartProducts', to='products.Product'),
        ),
    ]
