# Generated by Django 4.2 on 2023-05-24 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oders', '0007_orderitem_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='return_reason',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Out For Shipping', 'Out For Shipping'), ('Successfully Delivered', 'Successfully Delivered')], default='Pending', max_length=100, null=True),
        ),
    ]
