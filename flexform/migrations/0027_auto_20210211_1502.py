# Generated by Django 2.2.13 on 2021-02-11 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flexform', '0026_auto_20210211_1459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='image',
            field=models.ImageField(null=True, upload_to='uploads/images'),
        ),
    ]