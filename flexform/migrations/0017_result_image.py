# Generated by Django 2.2.13 on 2021-02-11 10:24

from django.db import migrations, models
import flexform.models


class Migration(migrations.Migration):

    dependencies = [
        ('flexform', '0016_auto_20210211_0940'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to="a"),
        ),
    ]
