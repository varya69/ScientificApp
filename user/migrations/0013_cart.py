# Generated by Django 3.2 on 2023-04-14 14:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_product_quantity'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ProductName', models.CharField(max_length=255)),
                ('Description', models.TextField()),
                ('Category', models.CharField(max_length=255)),
                ('Price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image', models.ImageField(blank=True, null=True, upload_to='products/')),
                ('quantity', models.IntegerField(default=1)),
                ('userId', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
        ),
    ]