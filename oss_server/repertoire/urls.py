from django.conf.urls import url, include
from django.urls import path
from repertoire.views import track_file

app_name = 'repertoire'
urlpatterns = [
    path('song_file/<int:pk>/', track_file, name='track_file')
]