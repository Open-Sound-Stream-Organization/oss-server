from typing import Union
from django.db.models import Model
from repertoire.api.ApiKey import ApiKey
from tastypie.http import HttpUnauthorized
from tastypie.authentication import Authentication
from django.core.exceptions import ObjectDoesNotExist


class ApiKeyOnlyAuthentication(Authentication):
    def is_authenticated(self, request, **kwargs):
        api_key = ApiKeyOnlyAuthentication.get_api_key(request)
        if isinstance(api_key, ApiKey):
            request.user = api_key.user
            return True
        else:
            return False

    @staticmethod
    def get_api_key(request) -> Union[ApiKey, bool]:
        if not(request.META.get('HTTP_AUTHORIZATION')):
            return False
        api_key_str = request.META['HTTP_AUTHORIZATION']
        try:
            api_key = ApiKey.objects.get(key=api_key_str)
        except ObjectDoesNotExist:
            return False
        return api_key


class ApiKeyOnlyOnSelfDelete(ApiKeyOnlyAuthentication):
    def is_authenticated(self, request, **kwargs) -> bool:
        if request.method == 'DELETE':
            if super(ApiKeyOnlyOnSelfDelete, self).is_authenticated(request, **kwargs):
                resolver_match: dict = request.resolver_match.kwargs
                if resolver_match.get('resource_name') == 'apikey' and resolver_match.get('pk', None) is not None:
                    return ApiKeyOnlyAuthentication.get_api_key(request).pk == resolver_match.get('pk')
                else:
                    return False
            else:
                return False
        else:
            return False
