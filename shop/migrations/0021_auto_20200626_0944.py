# Generated by Django 3.0.7 on 2020-06-26 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0020_auto_20200626_0934'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='firstname',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='lastname',
        ),
        migrations.AddField(
            model_name='customer',
            name='name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
