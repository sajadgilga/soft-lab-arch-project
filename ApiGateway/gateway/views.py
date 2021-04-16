# Create your views here.
from datetime import datetime

from django.core.exceptions import BadRequest
from django.http import HttpResponse
from django.views import View

from gateway.models import API


class MainGatewayView(View):

    def redirect(self, request):
        paths = request.path.split('/')
        if len(paths) < 2:
            raise BadRequest()
        api = API.objects.filter(name=paths[2])
        if api.count() != 1:
            raise BadRequest()
        if api.failure_strike >= 3:
            now = datetime.now()
            if (api.recent_failure_time - now).total_seconds() < 30:
                return HttpResponse('service unavailable', status=503)
            api.failure_strike = 0
            api.save()
        res = api.send_request(request, paths[3:].reduce(lambda a, b: str(a) + str(b)))
        if not res:
            return HttpResponse('service unavailable', status=503)
        return HttpResponse(res.json(), status=res.status_code)

    def get(self, request):
        return self.redirect(request)

    def post(self, request):
        return self.redirect(request)

    def put(self, request):
        return self.redirect(request)
