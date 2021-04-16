import json
from datetime import datetime

import requests
from django.db import models


# Create your models here.


class API(models.Model):
    name = models.CharField(max_length=128, blank=True, null=True)
    url = models.CharField(max_length=128)
    recent_failure_time = models.DateTimeField(null=True, blank=True)
    failure_strike = models.IntegerField(default=0)

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

        try:
            result = method_map[method](url, headers=headers, data=data, timeout=.5)
            self.failure_strike = 0
            self.save()
            return result
        except:
            self.failure_strike += 1
            self.recent_failure_time = datetime.now()
            self.save()
            return None

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name
