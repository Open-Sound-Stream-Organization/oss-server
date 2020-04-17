from django.conf.urls import url, include
from django.http import FileResponse
from django.urls import path
from django.views.generic import TemplateView

from web_interface.views import get_file_serve_view

app_name = 'web_interface'
urlpatterns = [
    url(r'^.*$', TemplateView.as_view(template_name='index.html'), name='react_index'),
]
serve_web_files = ['robots.txt', 'service-worker.js', 'manifest.json', 'asset-manifest.json']

for webfilename in serve_web_files:
    urlpatterns += [ path(webfilename, get_file_serve_view(webfilename)) ]