# Generated by Django 4.2 on 2023-05-07 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oders', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='product_price',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='total_price',
        ),
        migrations.AddField(
            model_name='order',
            name='total_price',
            field=models.FloatField(default=False),
        ),
    ]