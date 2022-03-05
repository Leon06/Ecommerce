# Generated by Django 2.2.3 on 2022-03-04 21:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import orders.common


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('carts', '0003_auto_20220302_1008'),
        ('promo_codes', '__first__'),
        ('shipping_addresses', '0003_auto_20220302_1008'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=100, unique=True)),
                ('status', models.CharField(choices=[(orders.common.OrderStatus('CREATED'), 'CREATED'), (orders.common.OrderStatus('PAYED'), 'PAYED'), (orders.common.OrderStatus('COMPLETED'), 'COMPLETED'), (orders.common.OrderStatus('CANCELED'), 'CANCELED')], default=orders.common.OrderStatus('CREATED'), max_length=50)),
                ('shipping_total', models.DecimalField(decimal_places=0, default=0, max_digits=8)),
                ('total', models.DecimalField(decimal_places=0, default=0, max_digits=8)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carts.Cart')),
                ('promo_code', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='promo_codes.PromoCode')),
                ('shipping_address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shipping_addresses.ShippingAddress')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Pedido',
                'verbose_name_plural': 'pedidos',
            },
        ),
    ]
