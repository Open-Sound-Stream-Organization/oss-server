from django.conf.urls import url, include
from django.urls import path
from django.views.generic import TemplateView

from repertoire.views import track_file

app_name = 'web_interface'
urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='react_index'),

]