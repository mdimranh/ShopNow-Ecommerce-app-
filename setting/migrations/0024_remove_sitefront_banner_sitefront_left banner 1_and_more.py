# Generated by Django 4.0 on 2022-01-01 16:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('setting', '0023_alter_slider_options_sitefront_banner_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sitefront',
            name='banner',
        ),
        migrations.AddField(
            model_name='sitefront',
            name='Left Banner 1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='left_banner1', to='setting.banner'),
        ),
        migrations.AddField(
            model_name='sitefront',
            name='Left Banner 2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='left_banner2', to='setting.banner'),
        ),
        migrations.AddField(
            model_name='sitefront',
            name='Top Banner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='top_banner', to='setting.banner'),
        ),
    ]