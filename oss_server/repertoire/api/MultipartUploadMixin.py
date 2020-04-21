from django.core.exceptions import MultipleObjectsReturned
from tastypie import http
from tastypie.exceptions import NotFound, BadRequest
from tastypie.utils.dict import dict_strip_unicode_keys


'''
Class from https://github.com/tomi77/django-tastypie-extras

The MIT License (MIT)

Copyright (c) 2016 Tomasz Jakub Rup

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''


class MultipartResourceMixin(object):
    """
    Resource with upload image possibility
    """
    def deserialize(self, request, data, format=None):  # pylint: disable=I0011,W0622
        """
        Given a request, data and a format, deserializes the given data.
        If content type is `multipart` then new behaviour, else old behaviour.
        """
        content_type = format or request.META.get('CONTENT_TYPE',
                                                  'application/json')

        if content_type == 'application/x-www-form-urlencoded':
            deserialized = request.POST
        elif content_type.startswith('multipart'):
            deserialized = request.POST.copy()
            deserialized.update(request.FILES)
        else:
            deserialized = super(MultipartResourceMixin, self) \
                .deserialize(request, data, format)

        return deserialized

    def put_detail(self, request, **kwargs):
        """
        Either updates an existing resource or creates a new one with the
        provided data.
        """
        try:
            body = request.body
        except Exception:  # pylint: disable=I0011,W0703
            body = None
        deserialized = self.deserialize(request, body,
                                        format=request.META.get('CONTENT_TYPE',
                                                                'application/json'))
        deserialized = self.alter_deserialized_detail_data(request,
                                                           deserialized)
        bundle = self.build_bundle(data=dict_strip_unicode_keys(deserialized),
                                   request=request)

        try:
            updated_bundle = self.obj_update(bundle=bundle,
                                             **self.remove_api_resource_names(kwargs))

            if not self._meta.always_return_data:
                return http.HttpNoContent()
            else:
                updated_bundle = self.full_dehydrate(updated_bundle)
                updated_bundle = self.alter_detail_data_to_serialize(request,
                                                                     updated_bundle)
                return self.create_response(request, updated_bundle)
        except (NotFound, MultipleObjectsReturned):
            updated_bundle = self.obj_create(bundle=bundle,
                                             **self.remove_api_resource_names(kwargs))
            location = self.get_resource_uri(updated_bundle)

            if not self._meta.always_return_data:
                return http.HttpCreated(location=location)
            else:
                updated_bundle = self.full_dehydrate(updated_bundle)
                updated_bundle = self.alter_detail_data_to_serialize(request,
                                                                     updated_bundle)
                return self.create_response(request, updated_bundle,
                                            response_class=http.HttpCreated,
                                            location=location)

    def post_list(self, request, **kwargs):
        """
        Creates a new resource/object with the provided data.
        """
        try:
            body = request.body
        except Exception:  # pylint: disable=I0011,W0703
            body = None
        deserialized = self.deserialize(request, body,
                                        format=request.META.get('CONTENT_TYPE',
                                                                'application/json'))
        deserialized = self.alter_deserialized_detail_data(request,
                                                           deserialized)
        bundle = self.build_bundle(data=dict_strip_unicode_keys(deserialized),
                                   request=request)

        updated_bundle = self.obj_create(bundle,
                                         **self.remove_api_resource_names(kwargs))
        location = self.get_resource_uri(updated_bundle)

        if not self._meta.always_return_data:
            return http.HttpCreated(location=location)
        else:
            updated_bundle = self.full_dehydrate(updated_bundle)
            updated_bundle = self.alter_detail_data_to_serialize(request,
                                                                 updated_bundle)
            return self.create_response(request, updated_bundle,
                                        response_class=http.HttpCreated,
                                        location=location)


