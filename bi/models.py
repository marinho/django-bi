import re

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse

from choices import *
from parsing import execute_query

class Query(models.Model):
    class Meta:
        verbose_name = _('Query')
        verbose_name_plural = _('Queries')

    title = models.CharField(max_length=50, blank=True, verbose_name=_('Title'))
    name = models.SlugField(unique=True, verbose_name=_('Name'))
    kind = models.CharField(
            max_length=10,
            choices=QUERY_KIND_CHOICES,
            default=QUERY_KIND_VISUAL,
            blank=True,
            db_index=True,
            verbose_name=_('Kind'),
            )
    content_type = models.ForeignKey(ContentType, null=True, blank=True, verbose_name=_('Content Type'))
    limit = models.IntegerField(blank=True, default=0, verbose_name=_('Limit'))
    url = models.CharField(max_length=200, default='', blank=True, verbose_name=_('URL'))
    embed_html = models.TextField(blank=True, verbose_name=_('Embed HTML'))
    
    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('bi_query_info', args=(self.name,))

    def get_value_fields(self):
        return [f.name for f in self.queryfield_set.all() if f.kind == QUERYFIELD_KIND_VALUE]

    def get_aggregation_fields(self):
        return [f for f in self.queryfield_set.all() if f.kind != QUERYFIELD_KIND_VALUE]

    def get_ordering_fields(self):
        return [f.kind + f.field_name for f in self.queryorder_set.all()]

    def get_conditions(self):
        return self.querycondition_set.all()

    def execute(self):
        return execute_query(self)

class QueryField(models.Model):
    class Meta:
        verbose_name = _('Field')
        verbose_name_plural = _('Fields')
        ordering = ('sequence',)

    query = models.ForeignKey(Query, verbose_name = _('Query'))
    name = models.CharField(max_length=50, db_index=True, verbose_name=_('Name'))
    title = models.CharField(max_length=50, blank=True, verbose_name=_('Title'))
    kind = models.CharField(
            max_length=10,
            choices=QUERYFIELD_KIND_CHOICES,
            default=QUERYFIELD_KIND_VALUE, 
            blank=True,
            db_index=True,
            verbose_name=_('Kind'),
            )
    expression = models.TextField(blank=True, verbose_name=_('Expression'))
    sequence = models.SmallIntegerField(default=0, blank=True, verbose_name=_('Sequence'))
    choices = models.TextField(
            blank=True,
            verbose_name=_('Choices'),
            help_text=_('JSON-formmated key/value dictionary with equivalent display values'),
            )

    @property
    def choices_dict(self):
        return eval(self.choices)

class QueryOrder(models.Model):
    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    query = models.ForeignKey(Query, verbose_name = _('Query'))
    field_name = models.CharField(max_length=50, verbose_name=_('Field Name'))
    kind = models.CharField(
            max_length=1,
            choices=QUERYORDER_KIND_CHOICES,
            default=QUERYORDER_KIND_ASC, 
            blank=True,
            db_index=True,
            verbose_name=_('Kind'),
            )

class QueryCondition(models.Model):
    class Meta:
        verbose_name = _('Condition')
        verbose_name_plural = _('Conditions')

    query = models.ForeignKey(Query, verbose_name = _('Query'))
    expression = models.CharField(max_length=200, verbose_name=_('Expression'))

