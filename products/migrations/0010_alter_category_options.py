# Generated by Django 5.0.6 on 2024-07-23 17:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_category_product_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
    ]
