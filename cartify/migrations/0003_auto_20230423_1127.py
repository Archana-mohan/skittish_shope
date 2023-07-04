# Generated by Django 3.2.16 on 2023-04-23 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cartify', '0002_cart_product_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='size',
            field=models.CharField(default=False, max_length=100),
        ),
        migrations.AlterField(
            model_name='cart',
            name='product_price',
            field=models.FloatField(default=False),
        ),
    ]