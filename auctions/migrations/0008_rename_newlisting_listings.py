# Generated by Django 5.0.1 on 2024-02-17 03:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_user_watchlist_delete_watchlist'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='NewListing',
            new_name='Listings',
        ),
    ]
