# Generated by Django 2.2.1 on 2019-06-24 10:22

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('publications', '0001_initial'),
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dimension',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_name', models.CharField(max_length=100, unique=True)),
                ('name', models.CharField(max_length=250)),
                ('name_en', models.CharField(max_length=250, null=True)),
                ('name_cs', models.CharField(max_length=250, null=True)),
                ('type', models.PositiveSmallIntegerField(choices=[(1, 'integer'), (2, 'text')])),
                ('desc', models.TextField(blank=True)),
                ('desc_en', models.TextField(blank=True, null=True)),
                ('desc_cs', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Metric',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_name', models.CharField(max_length=100, unique=True)),
                ('name', models.CharField(max_length=250)),
                ('name_en', models.CharField(max_length=250, null=True)),
                ('name_cs', models.CharField(max_length=250, null=True)),
                ('desc', models.TextField(blank=True)),
                ('desc_en', models.TextField(blank=True, null=True)),
                ('desc_cs', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReportType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_name', models.CharField(max_length=100, unique=True)),
                ('name', models.CharField(max_length=250)),
                ('name_en', models.CharField(max_length=250, null=True)),
                ('name_cs', models.CharField(max_length=250, null=True)),
                ('desc', models.TextField(blank=True)),
                ('desc_en', models.TextField(blank=True, null=True)),
                ('desc_cs', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReportTypeToDimension',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveSmallIntegerField()),
                ('dimension', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='logs.Dimension')),
                ('report_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='logs.ReportType')),
            ],
            options={
                'ordering': ('report_type', 'position', 'dimension'),
                'unique_together': {('report_type', 'dimension')},
            },
        ),
        migrations.AddField(
            model_name='reporttype',
            name='dimensions',
            field=models.ManyToManyField(related_name='report_types', through='logs.ReportTypeToDimension', to='logs.Dimension'),
        ),
        migrations.CreateModel(
            name='OrganizationPlatform',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sushi_credentials', django.contrib.postgres.fields.jsonb.JSONField(default=list)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizations.Organization')),
                ('platform', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='publications.Platform')),
            ],
        ),
        migrations.CreateModel(
            name='AccessLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dim1', models.IntegerField(blank=True, help_text='Value in dimension #1', null=True)),
                ('dim2', models.IntegerField(blank=True, help_text='Value in dimension #2', null=True)),
                ('dim3', models.IntegerField(blank=True, help_text='Value in dimension #3', null=True)),
                ('dim4', models.IntegerField(blank=True, help_text='Value in dimension #4', null=True)),
                ('dim5', models.IntegerField(blank=True, help_text='Value in dimension #5', null=True)),
                ('dim6', models.IntegerField(blank=True, help_text='Value in dimension #6', null=True)),
                ('dim7', models.IntegerField(blank=True, help_text='Value in dimension #7', null=True)),
                ('value', models.PositiveIntegerField(help_text='The value representing number of accesses')),
                ('date', models.DateField()),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('owner_level', models.PositiveSmallIntegerField(choices=[(100, 'Normal user'), (200, 'Robot'), (300, 'Organization admin'), (400, 'Consortium staff'), (1000, 'Consortium admin')], default=200, help_text='Level of user who created this record - used to determine who can modify it')),
                ('metric', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='logs.Metric')),
                ('report_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='logs.ReportType')),
                ('source', models.ForeignKey(help_text='Oranization and platform for which this log was created', on_delete=django.db.models.deletion.CASCADE, to='logs.OrganizationPlatform')),
                ('target', models.ForeignKey(help_text='Title for which this log was created', on_delete=django.db.models.deletion.CASCADE, to='publications.Title')),
            ],
        ),
        migrations.CreateModel(
            name='DimensionText',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('text', models.TextField(db_index=True)),
                ('text_local', models.TextField(blank=True)),
                ('text_local_en', models.TextField(blank=True, null=True)),
                ('text_local_cs', models.TextField(blank=True, null=True)),
                ('dimension', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='logs.Dimension')),
            ],
            options={
                'unique_together': {('dimension', 'text')},
            },
        ),
    ]
