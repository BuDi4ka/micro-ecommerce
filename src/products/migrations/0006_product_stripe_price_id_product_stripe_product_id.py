# Generated by Django 4.1.13 on 2025-06-21 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0005_productattachment_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="stripe_price_id",
            field=models.CharField(blank=True, max_length=220, null=True),
        ),
        migrations.AddField(
            model_name="product",
            name="stripe_product_id",
            field=models.CharField(blank=True, max_length=220, null=True),
        ),
    ]
