# Generated by Django 2.2.5 on 2019-11-06 09:47

from django.db import migrations, models
import django.db.models.deletion


def counter_report_type_superseeding_to_report_type_superseeding(apps, schema_editor):
    CounterReportType = apps.get_model('sushi', 'CounterReportType')
    for crt in CounterReportType.objects.filter(superseeded_by__isnull=False):
        crt.report_type.superseeded_by = crt.superseeded_by.report_type
        crt.report_type.save()


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0027_importbatch_interest_timestamp'),
        ('sushi', '0024_lock_level_change'),
    ]

    operations = [
        migrations.AddField(
            model_name='reporttype',
            name='superseeded_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='superseeds', to='logs.ReportType'),
        ),
        migrations.RunPython(counter_report_type_superseeding_to_report_type_superseeding, noop)
    ]
