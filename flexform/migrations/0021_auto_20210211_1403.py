# Generated by Django 2.2.13 on 2021-02-11 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flexform', '0020_auto_20210211_1356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='0fd4f10d7f8b308c49343502414d09e5'),
        ),
    ]
