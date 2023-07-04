# Generated by Django 3.2.16 on 2023-04-18 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_auto_20230406_2341'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='orginal_price',
        ),
        migrations.RemoveField(
            model_name='product',
            name='selling_price',
        ),
        migrations.AlterField(
            model_name='category',
            name='category_name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
