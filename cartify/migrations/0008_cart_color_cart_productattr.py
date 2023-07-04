# Generated by Django 4.2 on 2023-04-29 09:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0017_alter_productimage_image'),
        ('cartify', '0007_alter_cart_coupon'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='color',
            field=models.CharField(default=False, max_length=100),
        ),
        migrations.AddField(
            model_name='cart',
            name='productattr',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='products.productattribute'),
        ),
    ]
