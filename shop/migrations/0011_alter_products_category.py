# Generated by Django 5.1.5 on 2025-02-07 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_products_opinion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='category',
            field=models.CharField(choices=[('electronics', 'Elektronika'), ('fashion', 'Moda i odzież'), ('home_garden', 'Dom i ogród'), ('health_beauty', 'Zdrowie i uroda'), ('toys', 'Dziecko i zabawki'), ('sports', 'Sport i rekreacja'), ('automotive', 'Motoryzacja'), ('supermarket', 'Supermarket'), ('books', 'Książki i multimedia'), ('pets', 'Zwierzęta'), ('office_school', 'Biuro i szkoła')], max_length=255),
        ),
    ]
