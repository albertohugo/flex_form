# Generated by Django 2.2.13 on 2020-08-10 11:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('examples', '0003_auto_20200808_1117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='form',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Object',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=50)),
                ('type', models.PositiveSmallIntegerField(choices=[(1, 'String'), (2, 'Number')])),
                ('timestamp', models.DateField(auto_now_add=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='examples.Form')),
            ],
        ),
    ]
