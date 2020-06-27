# Generated by Django 3.0.5 on 2020-06-25 15:12

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0019_productvariantsize'),
    ]

    operations = [
        migrations.AddField(
            model_name='userproductvariantcart',
            name='size',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.ProductVariantSizeOption'),
            preserve_default=False,
        ),
    ]
