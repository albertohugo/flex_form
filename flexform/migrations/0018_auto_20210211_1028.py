# Generated by Django 2.2.13 on 2021-02-11 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flexform', '0017_result_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='profileimage'),
        ),
    ]
