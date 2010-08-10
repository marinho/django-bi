from django.utils.translation import ugettext as _

QUERY_KIND_VISUAL = 'visual'            # Makes a query using QuerySet and model configurations
QUERY_KIND_REDIRECT = 'redirect'        # Just makes a redirect to other URL
QUERY_KIND_EMBED = 'embed'              # Adds the embed HTML inside a box
QUERY_KIND_CHOICES = (
        (QUERY_KIND_VISUAL, _('Visual')),
        (QUERY_KIND_REDIRECT, _('Redirect to URL')),
        (QUERY_KIND_EMBED, _('Embed HTML')),
        )

QUERYFIELD_KIND_VALUE = 'value'
QUERYFIELD_KIND_SUM = 'sum'
QUERYFIELD_KIND_MIN = 'min'
QUERYFIELD_KIND_MAX = 'max'
QUERYFIELD_KIND_AVG = 'avg'
QUERYFIELD_KIND_COUNT = 'count'
QUERYFIELD_KIND_CHOICES = (
        (QUERYFIELD_KIND_VALUE, _('Value')),
        (QUERYFIELD_KIND_SUM, _('Sum')),
        (QUERYFIELD_KIND_MIN, _('Min')),
        (QUERYFIELD_KIND_MAX, _('Max')),
        (QUERYFIELD_KIND_AVG, _('Avg')),
        (QUERYFIELD_KIND_COUNT, _('Count')),
        )

QUERYORDER_KIND_ASC = ''
QUERYORDER_KIND_DESC = '-'
QUERYORDER_KIND_CHOICES = (
        (QUERYORDER_KIND_ASC, _('Asc')),
        (QUERYORDER_KIND_DESC, _('Desc')),
        )

