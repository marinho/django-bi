import random, datetime

from django.shortcuts import get_object_or_404
from django.conf import settings
from django.utils.datastructures import SortedDict
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from django.utils.translation import gettext as _
from django.utils.safestring import mark_safe

from djangoplus.utils.decorators import page

from models import Query
import app_settings

@page('bi/info.html')
def query_info(request, query_name):
    query = get_object_or_404(Query, name=query_name)
    title = query.title
    return locals()

def query_redirect(request, query_name):
    query = get_object_or_404(Query, name=query_name)

    if query.url:
        return HttpResponseRedirect(query.url)
    else:
        return HttpResponse('')

def query_embed(request, query_name):
    query = get_object_or_404(Query, name=query_name)

    if query.embed_html:
        ret = mark_safe(query.embed_html)
    
    return HttpResponse(ret or '')

@page('bi/list.html')
def query_list(request, query_name):
    query = get_object_or_404(Query, name=query_name)

    items = query.execute()
    items = [{'cells': [{
        'field_name': field.name,
        'value': item[field.name],
        'display': field.choices and field.choices_dict.get(item[field.name], None) or None,
        } for field in query.queryfield_set.all()],
        } for item in items]

    return locals()

def random_color(colors='0123456789ab'):
    return '#'+''.join([random.choice(colors) for i in range(6)])

def default_make_value(num, i):        
    return i[1]

class BIEncoder(simplejson.JSONEncoder):
    u"""This class is used to encode objects to JSON supporting date
    type values."""

    def default(self, obj):
        if isinstance(obj, datetime.date):
            return obj.strftime('%d/%m/%Y')
        return super(BIEncoder, self).default(obj)

def make_basic_chart_json(
        values,
        chart_type='pie',
        chart_tip='#val#',
        chart_nolabels=True,
        chart_make_value=default_make_value,
        chart_params=None,
        elements_params=None,
        ):
    # Sorts from biggest to smallest
    values = values.items()
    values.sort(lambda a,b: cmp(b[1], a[1]))
    values = SortedDict([(k,v) for k,v in values if v])
    
    data = {"bg_colour": "#ffffff",
            "elements": [{
              "type": chart_type,
              "tip": _(chart_tip),
              "no-labels": chart_nolabels,
              "colours": [random_color() for i in values.values()],
              "values": [chart_make_value(num, i) for num, i in enumerate(values.items())],
              "alpha": 0.7,
              }],
            }

    if chart_params:
        data.update(chart_params)

    if elements_params:
        for e in data['elements']:
            e.update(elements_params)

    return HttpResponse(simplejson.dumps(data, cls=BIEncoder), mimetype="text/javascript")

def make_pie_chart_json(values):
    def make_value(num, i):        
        return {
                'label': i[0],
                'value': i[1],
                'label-colour': '#000000',
                'font-size': num == 0 and 14 or 10,
                }

    return make_basic_chart_json(
            values,
            chart_type='pie',
            chart_tip='#label#<br>#val# of #total# (#percent# of total)',
            chart_make_value=make_value,
            elements_params={
              "start-angle": 35,
              "animate": [{"type": "fade"}, { "type": "bounce", "distance": 5 }],
                },
            )

def make_bar_chart_json(values):
    def make_value(num, i):        
        return {
                'top': i[1],
                'colour': random_color(),
                }

    # Makes x-axis labels
    x_axis = {
            'labels': {
                'labels': values.keys(),
                },
            '3d': 5,
            "colour": "#909090",
            }

    # Max y-axis
    y_axis = {
            "max": max(values.values()),
            }

    return make_basic_chart_json(
            values,
            chart_type='bar_3d',
            chart_nolabels=False,
            chart_make_value=make_value,
            chart_params={"x_axis": x_axis, "y_axis": y_axis},
            )

@page('bi/chart_pie.html')
def query_chart_pie(request, query_name):
    query = get_object_or_404(Query, name=query_name)
    
    if 'data' in request.GET:
        fields = query.queryfield_set.all()

        def get_display(field, value):
            return field.choices and field.choices_dict.get(value, value) or value

        items = query.execute()
        items = dict([(
            get_display(fields[0], item[fields[0].name]),
            get_display(fields[1], item[fields[1].name]),
            ) for item in items])

        return make_pie_chart_json(items)

    else:
        data_url = "%s?data"%request.path_info
        OPENFLASHCHART_SWF_URL = settings.MEDIA_URL + app_settings.OPENFLASHCHART_SWF_URL

    return locals()

@page('bi/chart_bar.html')
def query_chart_bar(request, query_name):
    query = get_object_or_404(Query, name=query_name)
    
    if 'data' in request.GET:
        fields = query.queryfield_set.all()

        def get_display(field, value):
            return field.choices and field.choices_dict.get(value, value) or value

        items = query.execute()
        items = dict([(
            get_display(fields[0], item[fields[0].name]),
            get_display(fields[1], item[fields[1].name]),
            ) for item in items])

        return make_bar_chart_json(items)

    else:
        data_url = "%s?data"%request.path_info
        OPENFLASHCHART_SWF_URL = settings.MEDIA_URL + app_settings.OPENFLASHCHART_SWF_URL

    return locals()

