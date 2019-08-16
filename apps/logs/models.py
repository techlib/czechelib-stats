from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.functional import cached_property
from django.utils.timezone import now

from core.models import USER_LEVEL_CHOICES, UL_ROBOT, DataSource
from organizations.models import Organization
from publications.models import Platform, Title


class OrganizationPlatform(models.Model):

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)
    sushi_credentials = JSONField(default=list)

    def __str__(self):
        return f'{self.organization} | {self.platform}'


class ReportType(models.Model):

    """
    Represents type of report, such as 'TR' or 'DR' in Sushi
    """

    short_name = models.CharField(max_length=100)
    name = models.CharField(max_length=250)
    desc = models.TextField(blank=True)
    dimensions = models.ManyToManyField('Dimension', related_name='report_types',
                                        through='ReportTypeToDimension')
    source = models.ForeignKey(DataSource, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        unique_together = (('short_name', 'source'),)

    def __str__(self):
        return self.short_name

    @cached_property
    def dimension_short_names(self):
        return [dim.short_name for dim in self.dimensions.all()]

    @cached_property
    def dimensions_sorted(self):
        return list(self.dimensions.all())


class InterestGroup(models.Model):

    """
    Describes a measure of interest of users. It is assigned to Metrics which are
    deemed as interest-defining. If more metrics refer to the same InterestGroup
    they are treated as describing the same interest.
    There will for instance be interest in books which would be described by different
    metrics in COUNTER 4 and 5, then there will be the interest in databases, etc.
    """
    short_name = models.CharField(max_length=100)
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Metric(models.Model):

    """
    Type of metric, such as 'Unique_Item_Requests', etc.
    """

    short_name = models.CharField(max_length=100)
    name = models.CharField(max_length=250, blank=True)
    desc = models.TextField(blank=True)
    active = models.BooleanField(default=True,
                                 help_text='Only active metrics are reported to users')
    interest_group = models.ForeignKey(
        InterestGroup, null=True, blank=True, on_delete=models.SET_NULL,
        help_text='If given, it marks the metric as representing interest of the specified type'
    )
    name_in_interest_group = models.CharField(
        max_length=250, blank=True,
        help_text='How is the metric called when interest sub-series are shown'
    )
    source = models.ForeignKey(DataSource, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        unique_together = (('short_name', 'source'),)

    def __str__(self):
        return self.short_name


class Dimension(models.Model):

    """
    Represents a specific dimension of multidimensional data
    """

    TYPE_INT = 1
    TYPE_TEXT = 2

    DIMENSION_TYPE_CHOICES = (
        (TYPE_INT, 'integer'),
        (TYPE_TEXT, 'text'),
    )

    short_name = models.CharField(max_length=100)
    name = models.CharField(max_length=250)
    type = models.PositiveSmallIntegerField(choices=DIMENSION_TYPE_CHOICES)
    desc = models.TextField(blank=True)
    source = models.ForeignKey(DataSource, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ('reporttypetodimension', )
        unique_together = (('short_name', 'source'),)

    def __str__(self):
        return '{} ({})'.format(self.short_name, self.get_type_display())


class ReportTypeToDimension(models.Model):

    """
    Intermediate model to facilitate connection between report_type and dimension with
    additional position attribute
    """

    report_type = models.ForeignKey(ReportType, on_delete=models.CASCADE)
    dimension = models.ForeignKey(Dimension, on_delete=models.CASCADE)
    position = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = (('report_type', 'dimension'), )
        ordering = ('position',)

    def __str__(self):
        return '{}-{} #{}'.format(self.report_type, self.dimension, self.position)


class ImportBatch(models.Model):

    """
    Represents one batch of imported data. Such data share common source, such as a file
    and the user who created them.
    """

    created = models.DateTimeField(default=now)
    system_created = models.BooleanField(default=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                             on_delete=models.SET_NULL)
    owner_level = models.PositiveSmallIntegerField(
        choices=USER_LEVEL_CHOICES,
        default=UL_ROBOT,
        help_text='Level of user who created this record - used to determine who can modify it'
    )

    class Meta:
        verbose_name_plural = "Import batches"

    def clean(self):
        super().clean()
        if not self.system_created and not self.user:
            raise ValidationError('When system_created is False, user must be filled in')

    @cached_property
    def accesslog_count(self):
        return self.accesslog_set.count()


class AccessLog(models.Model):

    report_type = models.ForeignKey(ReportType, on_delete=models.CASCADE)
    metric = models.ForeignKey(Metric, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE, null=True)
    target = models.ForeignKey(Title, on_delete=models.CASCADE,
                               help_text='Title for which this log was created')
    dim1 = models.IntegerField(null=True, blank=True, help_text='Value in dimension #1')
    dim2 = models.IntegerField(null=True, blank=True, help_text='Value in dimension #2')
    dim3 = models.IntegerField(null=True, blank=True, help_text='Value in dimension #3')
    dim4 = models.IntegerField(null=True, blank=True, help_text='Value in dimension #4')
    dim5 = models.IntegerField(null=True, blank=True, help_text='Value in dimension #5')
    dim6 = models.IntegerField(null=True, blank=True, help_text='Value in dimension #6')
    dim7 = models.IntegerField(null=True, blank=True, help_text='Value in dimension #7')
    value = models.PositiveIntegerField(help_text='The value representing number of accesses')
    date = models.DateField()
    # internal fields
    created = models.DateTimeField(default=now)
    owner_level = models.PositiveSmallIntegerField(
        choices=USER_LEVEL_CHOICES,
        default=UL_ROBOT,
        help_text='Level of user who created this record - used to determine who can modify it'
    )
    import_batch = models.ForeignKey(ImportBatch, on_delete=models.CASCADE)


class DimensionText(models.Model):
    """
    Mapping between text value and integer values for a specific dimension
    """

    id = models.AutoField(primary_key=True)
    dimension = models.ForeignKey(Dimension, on_delete=models.CASCADE)
    text = models.TextField(db_index=True)
    text_local = models.TextField(blank=True)

    class Meta:
        unique_together = (("dimension", "text"),)

    def __str__(self):
        if self.text_local:
            return self.text_local
        return self.text
