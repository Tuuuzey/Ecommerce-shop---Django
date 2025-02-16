# Generated by Django 5.1.5 on 2025-01-18 13:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_alter_products_discount_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='discount_price',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(99999.99)]),
        ),
    ]
