# Generated by Django 4.0 on 2021-12-28 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_wishlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopcart',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default='2021-12-28 11:32:11.107007'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='wishlist',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default='2021-12-28 11:32:11.107007'),
            preserve_default=False,
        ),
    ]