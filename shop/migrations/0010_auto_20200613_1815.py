# Generated by Django 3.0.7 on 2020-06-13 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_customer_order_orderitem_shippingaddress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='less_price',
            field=models.FloatField(default=0),
        ),
    ]
