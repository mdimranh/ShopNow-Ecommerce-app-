# Generated by Django 4.0.1 on 2022-04-12 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setting', '0002_currency'),
    ]

    operations = [
        migrations.AddField(
            model_name='currency',
            name='rate',
            field=models.FloatField(default=1),
        ),
    ]