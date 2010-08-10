# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('bi.views',
    url(r'^([\w_-]+)/$', 'query_info', name='bi_query_info'),
    url(r'^([\w_-]+)/redirect/$', 'query_redirect', name='bi_query_redirect'),
    url(r'^([\w_-]+)/embed/$', 'query_embed', name='bi_query_embed'),
    url(r'^([\w_-]+)/list/$', 'query_list', name='bi_query_list'),
    url(r'^([\w_-]+)/chart-pie/$', 'query_chart_pie', name='bi_query_chart_pie'),
    url(r'^([\w_-]+)/chart-bar/$', 'query_chart_bar', name='bi_query_chart_bar'),
    #url('([\w_-]+)/report/$', 'query_report', name='bi_query_report'),
)

