# Generated by Django 4.2 on 2023-06-30 08:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cartify', '0010_cart_discount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='discount',
        ),
    ]
