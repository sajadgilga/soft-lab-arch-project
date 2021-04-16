# Create your views here.
from datetime import datetime
from functools import reduce

from django.http import HttpResponse
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from gateway.models import API


class MainGatewayView(APIView):

    def redirect(self, request):
        paths = request.path.split('/')
        if len(paths) < 2:
            raise ValidationError('incorrect path format')
        api = API.objects.filter(name=paths[2])
        if api.count() != 1:
            raise ValidationError('multiple api found for this service name')
        api = api[0]
        if api.failure_strike >= 3:
            now = datetime.now()
            if (api.recent_failure_time - now).total_seconds() < 30:
                return Response('service unavailable', status=503)
            api.failure_strike = 0
            api.save()
        print(paths, reduce(lambda a, b: f'{str(a)}/{str(b)}', paths[3:]))

        res = api.send_request(request, reduce(lambda a, b: f'{str(a)}/{str(b)}', paths[3:]))
        if res == -1:
            return Response('service unavailable', status=503)
        if res.headers.get('Content-Type', '').lower() == 'application/json':
            data = res.json()
        else:
            data = res.content
        return Response(data, status=res.status_code)

    def get(self, request):
        return self.redirect(request)

    def post(self, request):
        return self.redirect(request)

    def put(self, request):
        return self.redirect(request)
