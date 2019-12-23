# Generated by Django 2.2.9 on 2019-12-23 15:53

from django.db import migrations, models
import django.db.models.deletion


def create_platformtitle_from_accesslogs(apps, schema_editor):
    AccessLog = apps.get_model('logs', 'AccessLog')
    PlatformTitle = apps.get_model('publications', 'PlatformTitle')
    pts = []
    for rec in AccessLog.objects.exclude(target__isnull=True).\
            values('platform_id', 'target_id', 'organization_id', 'date').distinct().iterator():
        pts.append(PlatformTitle(
            platform_id=rec['platform_id'],
            title_id=rec['target_id'],
            organization_id=rec['organization_id'],
            date=rec['date'],
        ))
        # we process in batches of 1000 to save memory
        if len(pts) > 1000:
            PlatformTitle.objects.bulk_create(pts)
            pts = []
    PlatformTitle.objects.bulk_create(pts)


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0013_auto_20191113_0939'),
        ('publications', '0014_remove_old_interest_reports_attr'),
        ('logs', '0032_optimize_accesslog_indexes'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlatformTitle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(help_text='Month for which title was available on platform')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizations.Organization')),
                ('platform', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='publications.Platform')),
                ('title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='publications.Title')),
            ],
        ),

        migrations.RunPython(create_platformtitle_from_accesslogs, noop)
    ]
