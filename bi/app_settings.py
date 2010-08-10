from django.conf import settings

OPENFLASHCHART_SWF_URL = getattr(settings, 'OPENFLASHCHART_SWF_URL', 'extras/open-flash-chart/open-flash-chart.swf')

