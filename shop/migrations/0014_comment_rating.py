# Generated by Django 5.1.5 on 2025-02-08 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0013_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='rating',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=2, null=True),
        ),
    ]
