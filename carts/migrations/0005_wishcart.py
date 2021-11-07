# Generated by Django 3.2.7 on 2021-11-06 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0004_wishlist'),
    ]

    operations = [
        migrations.CreateModel(
            name='WishCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wishcart_id', models.CharField(blank=True, max_length=250)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
