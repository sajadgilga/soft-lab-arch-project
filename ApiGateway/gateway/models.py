import json

import requests
from django.db import models


# Create your models here.

class API(models.Model):
    name = models.CharField(max_length=128, blank=True, null=True)
    url = models.CharField(max_length=128)

    def send_request(self, request, path):
        headers = {'authorization': request.META.get('HTTP_AUTHORIZATION')}

        url = self.url + path
        method = request.method.lower()
        method_map = {
            'get': requests.get,
            'post': requests.post,
            'put': requests.put,
            'delete': requests.delete
        }

        if request.content_type and request.content_type.lower() == 'application/json':
            data = json.dumps(request.data)
            headers['content-type'] = request.content_type
        else:
            data = request.data

        return method_map[method](url, headers=headers, data=data, timeout=.5)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name
