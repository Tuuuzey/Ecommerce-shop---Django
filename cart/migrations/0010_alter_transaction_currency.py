# Generated by Django 5.1.5 on 2025-02-01 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0009_remove_promocode_times_of_use'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='currency',
            field=models.CharField(default='USD', max_length=100),
        ),
    ]
