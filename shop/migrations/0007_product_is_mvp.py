# Generated by Django 3.0.7 on 2020-06-12 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_categorey_is_published'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_mvp',
            field=models.BooleanField(default=False),
        ),
    ]