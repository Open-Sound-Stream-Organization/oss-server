from django.http import FileResponse
from django.shortcuts import render

def get_file_serve_view(filename:str):
    def get_file(request):
        return FileResponse(open('web_interface/oss-web/build/{}'.format(filename), 'rb'))
    return get_file

