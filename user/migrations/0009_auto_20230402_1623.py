# Generated by Django 3.2 on 2023-04-02 10:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_alter_product_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='category',
            new_name='Category',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='description',
            new_name='Description',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='price',
            new_name='Price',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='name',
            new_name='ProductName',
        ),
    ]