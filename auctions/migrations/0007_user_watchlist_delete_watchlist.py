# Generated by Django 5.0.1 on 2024-02-17 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_watchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='watchlist',
            field=models.ManyToManyField(blank=True, to='auctions.newlisting'),
        ),
        migrations.DeleteModel(
            name='Watchlist',
        ),
    ]
