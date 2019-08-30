# Generated by Django 2.2.4 on 2019-08-29 10:40

from django.db import migrations, models
from django.db.models import F


def fill_processing_success_from_download_success(apps, schema_editor):
    SushiFetchAttempt = apps.get_model('sushi', 'SushiFetchAttempt')
    SushiFetchAttempt.objects.all().update(processing_success=F('download_success'))


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('sushi', '0013_auto_20190829_1105'),
    ]

    operations = [
        migrations.AddField(
            model_name='sushifetchattempt',
            name='processing_success',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.RunPython(fill_processing_success_from_download_success, noop)
    ]