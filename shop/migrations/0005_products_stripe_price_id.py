# Generated by Django 5.1.5 on 2025-02-01 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_alter_products_discount_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='stripe_price_id',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
