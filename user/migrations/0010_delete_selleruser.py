# Generated by Django 5.1.5 on 2025-02-10 18:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0015_alter_products_seller'),
        ('user', '0009_remove_selleruser_email'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SellerUser',
        ),
    ]
