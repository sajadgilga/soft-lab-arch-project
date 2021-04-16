from rest_framework.views import APIView

from users.serializers import UserSerializer


class ProfileView(APIView):
    def serializer_class(self):
        return UserSerializer

    def get(self, request):
        user = request.user
        return self.serializer_class()(user).data

    def post(self, request):
        pass
