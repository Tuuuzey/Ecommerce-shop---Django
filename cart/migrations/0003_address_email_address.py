# Generated by Django 5.1.5 on 2025-01-27 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_alter_address_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='email_address',
            field=models.CharField(default='test', max_length=254),
        ),
    ]
