# Generated by Django 3.2 on 2023-03-14 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20230314_2028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seller',
            name='SellerId',
            field=models.AutoField(default=1, primary_key=True, serialize=False),
        ),
    ]
