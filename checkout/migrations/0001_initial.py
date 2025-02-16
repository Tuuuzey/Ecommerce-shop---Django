# Generated by Django 5.1.5 on 2025-02-05 19:02

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shop', '0005_products_stripe_price_id'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PromoCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50)),
                ('value', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('username', models.CharField(max_length=150)),
                ('email', models.CharField(max_length=254)),
                ('address', models.CharField(max_length=300)),
                ('phone_number', models.IntegerField(validators=[django.core.validators.MinValueValidator(1000000), django.core.validators.MaxValueValidator(999999999999999)])),
                ('country', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=200, null=True)),
                ('city', models.CharField(max_length=200)),
                ('zip', models.CharField(max_length=9)),
                ('preparing', models.BooleanField(null=True)),
                ('on_the_way', models.BooleanField(null=True)),
                ('delivered', models.BooleanField(null=True)),
                ('id_username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('preparing', 'Preparing'), ('on_the_way', 'On the Way'), ('delivered', 'Delivered'), ('canceled', 'Canceled')], default='pending', max_length=20)),
                ('total', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)])),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='checkout.address')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('promo_code', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='checkout.promocode')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('price', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)])),
                ('discount_price', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='checkout.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.products')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id_transaction', models.AutoField(primary_key=True, serialize=False)),
                ('method', models.CharField(max_length=200)),
                ('status', models.CharField(max_length=20)),
                ('total', models.FloatField()),
                ('currency', models.CharField(default='USD', max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('id_username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='checkout.address')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='transaction',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='checkout.transaction'),
        ),
    ]
