# Generated by Django 4.1 on 2022-11-27 03:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0009_historicalpurchase_historicalorder_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historicalpurchase',
            old_name='payed',
            new_name='balance',
        ),
        migrations.RenameField(
            model_name='purchase',
            old_name='payed',
            new_name='balance',
        ),
    ]
