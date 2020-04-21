from django.core.exceptions import ObjectDoesNotExist
from django.http import FileResponse, HttpResponseForbidden, HttpResponseNotFound
from django.shortcuts import get_object_or_404

from repertoire.api.ApiKey import ApiKey
from repertoire.models import Track


def track_file(request, pk: int):
    '''
    Function to serve track files to authenticated users
    :param request: HTTP-Request object
    :param pk: Primary Key of requested track file
    :return: FileResponse of Audio File if authorized, else HTTP Error 403 or HTTP Error 404 if no fitting track is found based on
    '''
    if request.META.get('HTTP_AUTHORIZATION'):
        api_key_str = request.META['HTTP_AUTHORIZATION']
        try:
            api_key = ApiKey.objects.get(key=api_key_str)
        except ObjectDoesNotExist:
            return HttpResponseForbidden("<b>Forbidden:</b> Invalid API-Key!")
        request.user = api_key.user
        track = get_object_or_404(Track, id=pk, user=api_key.user)
        try:
            return FileResponse(track.audio.open("rb"))
        except ValueError:
            return HttpResponseNotFound(
                "<b>Not found:</b> For the requested track no audio file was saved on the server")
    else:
        if request.user.is_authenticated:
            track = get_object_or_404(Track, id=pk, user=request.user)
            try:
                return FileResponse(track.audio.open("rb"))
            except ValueError:
                return HttpResponseNotFound(
                    "<b>Not found:</b> For the requested track no audio file was saved on the server")
        return HttpResponseForbidden("<b>Forbidden:</b> Authorized access with an API-Key only!")
