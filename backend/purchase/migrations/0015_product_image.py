# Generated by Django 4.0 on 2022-10-20 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0014_barcycle_closing_report_barcycle_opening_report'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, default='products/default.png', null=True, upload_to='products/'),
        ),
    ]
