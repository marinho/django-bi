import re

from django.db import models

from choices import *

EXP_EQUAL = re.compile('([\w_]+)[ ]*=[ ]*(.+)', re.I)
EXP_NOTEQUAL = re.compile('([\w_]+)[ ]*(<>|!=)[ ]*(.+)', re.I)
EXP_GT = re.compile('([\w_]+)[ ]*>[ ]*(.+)', re.I)
EXP_GTE = re.compile('([\w_]+)[ ]*>=[ ]*(.+)', re.I)
EXP_LT = re.compile('([\w_]+)[ ]*<[ ]*(.+)', re.I)
EXP_LTE = re.compile('([\w_]+)[ ]*<=[ ]*(.+)', re.I)
EXP_CONTAINS = re.compile('([\w_]+)[ ]*contains[ ]*(.+)', re.I)
EXP_STARTSWITH = re.compile('([\w_]+)[ ]*starts[ ]*with[ ]*(.+)', re.I)
EXP_ENDSWITH = re.compile('([\w_]+)[ ]*ends[ ]*with[ ]*(.+)', re.I)
EXP_NOTCONTAINS = re.compile('([\w_]+)[ ]*not[ ]*contains[ ]*(.+)', re.I)
EXP_NOTSTARTSWITH = re.compile('([\w_]+)[ ]*not[ ]*starts[ ]*with[ ]*(.+)', re.I)
EXP_NOTENDSWITH = re.compile('([\w_]+)[ ]*not[ ]*ends[ ]*with[ ]*(.+)', re.I)

def parse_condition_value(val):
    """Parses know values to transform in respective Python values"""

    if val.lower() == 'true':
        return True
    elif val.lower() == 'false':
        return False
        
    return val

def parse_annotate_from_field(f):
    """Parses aggregation functions to transform in annotation fields"""
    if f.kind == QUERYFIELD_KIND_SUM:
        return models.Sum(f.expression or f.name)
    elif f.kind == QUERYFIELD_KIND_MIN:
        return models.Min(f.expression or f.name)
    elif f.kind == QUERYFIELD_KIND_MAX:
        return models.Max(f.expression or f.name)
    elif f.kind == QUERYFIELD_KIND_AVG:
        return models.Avg(f.expression or f.name)
    elif f.kind == QUERYFIELD_KIND_COUNT:
        return models.Count(f.expression or f.name)

def parse_condition(expr, qs):
    """Parses a condition expression and attach a queryset method call to given queryset"""

    # Filter
    if EXP_EQUAL.match(expr):
        m = EXP_EQUAL.match(expr)
        qs = qs.filter(**{str(m.group(1)): parse_condition_value(m.group(2))})

    elif EXP_NOTEQUAL.match(expr):
        m = EXP_NOTEQUAL.match(expr)
        qs = qs.exclude(**{str(m.group(1)): parse_condition_value(m.group(3))})

    elif EXP_GTE.match(expr):
        m = EXP_GTE.match(expr)
        qs = qs.filter(**{str(m.group(1))+'__gte': parse_condition_value(m.group(2))})

    elif EXP_GT.match(expr):
        m = EXP_GT.match(expr)
        qs = qs.filter(**{str(m.group(1))+'__gt': parse_condition_value(m.group(2))})

    elif EXP_LTE.match(expr):
        m = EXP_LTE.match(expr)
        qs = qs.filter(**{str(m.group(1))+'__lte': parse_condition_value(m.group(2))})

    elif EXP_LT.match(expr):
        m = EXP_LT.match(expr)
        qs = qs.filter(**{str(m.group(1))+'__lt': parse_condition_value(m.group(2))})

    elif EXP_CONTAINS.match(expr):
        m = EXP_CONTAINS.match(expr)
        qs = qs.filter(**{str(m.group(1))+'__icontains': parse_condition_value(m.group(2))})

    elif EXP_STARTSWITH.match(expr):
        m = EXP_STARTSWITH.match(expr)
        qs = qs.filter(**{str(m.group(1))+'__istartswith': parse_condition_value(m.group(2))})

    elif EXP_ENDSWITH.match(expr):
        m = EXP_ENDSWITH.match(expr)
        qs = qs.filter(**{str(m.group(1))+'__iendswith': parse_condition_value(m.group(2))})

    # Exclude

    elif EXP_NOTCONTAINS.match(expr):
        m = EXP_NOTCONTAINS.match(expr)
        qs = qs.exclude(**{str(m.group(1))+'__icontains': parse_condition_value(m.group(2))})

    elif EXP_NOTSTARTSWITH.match(expr):
        m = EXP_NOTSTARTSWITH.match(expr)
        qs = qs.exclude(**{str(m.group(1))+'__istartswith': parse_condition_value(m.group(2))})

    elif EXP_NOTENDSWITH.match(expr):
        m = EXP_NOTENDSWITH.match(expr)
        qs = qs.exclude(**{str(m.group(1))+'__iendswith': parse_condition_value(m.group(2))})

    return qs

def execute_query_visual(query):
    """Execute a query with 'Visual' kind"""
    model = query.content_type.model_class()

    # Starts the queryset
    qs = model.objects.all()

    # Values/groupping fields
    v_fields = query.get_value_fields()
    if v_fields:
        qs = qs.values(*v_fields)

    # Aggregation fields
    annotate = dict([(str(f.name), parse_annotate_from_field(f)) for f in query.get_aggregation_fields()
        if f.kind != QUERYFIELD_KIND_VALUE])
    if annotate:
        qs = qs.annotate(**annotate)

    # Ordering fields
    o_fields = query.get_ordering_fields()
    if o_fields:
        qs = qs.order_by(*o_fields)

    # Condition expressions
    for cond in query.get_conditions():
        qs = parse_condition(cond.expression, qs)

    # Limit slacing
    if query.limit > 0:
        qs = qs[:query.limit]

    return list(qs)

def execute_query(query):
    if query.kind == QUERY_KIND_VISUAL:
        return execute_query_visual(query)

