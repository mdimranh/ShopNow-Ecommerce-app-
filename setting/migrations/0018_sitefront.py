# Generated by Django 4.0 on 2021-12-31 17:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('setting', '0017_slidersetting_autoplay_timeout'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteFront',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slider', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='setting.slider')),
            ],
            options={
                'verbose_name': 'Site Front',
            },
        ),
    ]