# Generated by Django 3.2.7 on 2021-10-29 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_auto_20211028_1343'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='coupon_use_status',
            field=models.BooleanField(default=False),
        ),
    ]
