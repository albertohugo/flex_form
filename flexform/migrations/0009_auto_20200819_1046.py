# Generated by Django 2.2.13 on 2020-08-19 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flexform', '0008_result_id_result'),
    ]

    operations = [
        migrations.AddField(
            model_name='form',
            name='private',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='form',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]