# Generated by Django 3.2.7 on 2021-10-30 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_order_coupon_use_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='discount_amount',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='nett_paid',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
