# Generated by Django 4.2 on 2023-06-21 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oders', '0009_orderitem_delivered_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Out For Shipping', 'Out For Shipping'), ('Successfully Delivered', 'Successfully Delivered'), ('Shipped', 'Shipped')], default='Pending', max_length=100),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Out For Shipping', 'Out For Shipping'), ('Successfully Delivered', 'Successfully Delivered'), ('Shipped', 'Shipped')], default='Pending', max_length=100, null=True),
        ),
    ]