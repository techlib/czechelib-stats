# Generated by Django 2.2.5 on 2019-11-13 08:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0013_auto_20191113_0939'),
        ('publications', '0014_remove_old_interest_reports_attr'),
        ('cost', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='payment',
            unique_together={('organization', 'platform', 'year')},
        ),
    ]