# Generated by Django 5.1.3 on 2025-02-03 22:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0008_alter_auctionlisting_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="auctionlisting",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="auctions.category",
            ),
        ),
    ]
