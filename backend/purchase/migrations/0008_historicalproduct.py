# Generated by Django 4.0 on 2022-11-25 14:50

import colorfield.fields
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('purchase', '0007_historicalreport_historicalhappen_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalProduct',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=20)),
                ('price', models.FloatField(default=0)),
                ('color', colorfield.fields.ColorField(default='#ffdd00', image_field=None, max_length=18, samples=None)),
                ('active', models.BooleanField(default=True)),
                ('image', models.TextField(blank=True, default='products/default.png', max_length=100, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='auth.user')),
            ],
            options={
                'verbose_name': 'historical product',
                'verbose_name_plural': 'historical Producten',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
