# Generated by Django 2.2.13 on 2021-02-11 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flexform', '0021_auto_20210211_1403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/<django.db.models.fields.related.ForeignKey>68a7eabd10f2d02870ee19588a244f77'),
        ),
    ]
