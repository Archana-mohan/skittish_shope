# Generated by Django 4.2 on 2023-05-25 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0019_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]),
        ),
    ]
