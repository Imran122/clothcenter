# Generated by Django 3.0.7 on 2020-06-11 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_product_is_published'),
    ]

    operations = [
        migrations.AddField(
            model_name='categorey',
            name='is_published',
            field=models.BooleanField(default=True),
        ),
    ]