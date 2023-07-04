# Generated by Django 4.2 on 2023-05-03 08:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0017_alter_productimage_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productattribute',
            name='sizevariant',
        ),
        migrations.AddField(
            model_name='productattribute',
            name='sizevariant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='products.sizevariant'),
        ),
    ]
