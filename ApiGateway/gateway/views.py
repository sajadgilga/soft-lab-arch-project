# Create your views here.
from django.views import View


class MainGatewayView(View):
    def redirect(self, request):
        pass

    def get(self, request):
        return self.redirect(request)

    def post(self, request):
        return self.redirect(request)

    def put(self, request):
        return self.redirect(request)
