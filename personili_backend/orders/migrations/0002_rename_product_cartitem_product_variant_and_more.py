# Generated by Django 5.0 on 2024-07-21 17:21

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="cartitem",
            old_name="product",
            new_name="product_variant",
        ),
        migrations.RemoveField(
            model_name="cart",
            name="total_amount",
        ),
    ]
