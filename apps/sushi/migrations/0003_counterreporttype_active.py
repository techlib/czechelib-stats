# Generated by Django 2.2.4 on 2019-08-02 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sushi', '0002_sushifetchattempt'),
    ]

    operations = [
        migrations.AddField(
            model_name='counterreporttype',
            name='active',
            field=models.BooleanField(default=True, help_text='When turned off, this type of report will not be automatically downloaded'),
        ),
    ]
