# Generated by Django 4.2 on 2023-05-17 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0005_alter_address_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='username',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
