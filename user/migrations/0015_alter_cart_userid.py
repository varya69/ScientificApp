# Generated by Django 3.2 on 2023-04-14 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0014_cart_productid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='userId',
            field=models.IntegerField(default=1),
        ),
    ]
