# Generated by Django 4.0 on 2021-12-29 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setting', '0009_siteconfiguration_alter_area_name_alter_city_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteconfiguration',
            name='site_phone',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]