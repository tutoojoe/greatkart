# Generated by Django 3.2.7 on 2021-11-08 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_alter_product_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='images',
            field=models.ImageField(blank=True, default='photos/products/default_product.png', null=True, upload_to='photos/products'),
        ),
    ]
