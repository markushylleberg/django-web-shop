# Generated by Django 3.0.5 on 2020-05-08 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_userproductvariantcart'),
    ]

    operations = [
        migrations.AddField(
            model_name='userproductvariantcart',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
