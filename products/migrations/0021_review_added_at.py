# Generated by Django 4.2 on 2023-05-25 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0020_alter_review_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='added_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
