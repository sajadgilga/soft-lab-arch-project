from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import UserSerializer


class RegisterView(APIView):
    def get_serializer_class(self):
        return UserSerializer

    def get_serializer(self, data):
        return self.get_serializer_class()(data=data)

    def serialize(self, instance):
        return self.get_serializer_class()(instance).data

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(self.serialize(user))


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return UserSerializer

    def get_serializer(self, instance, data):
        return self.get_serializer_class()(instance, data=data, partial=True)

    def serialize(self, instance):
        return self.get_serializer_class()(instance).data

    def get(self, request):
        user = request.user
        return Response(self.serialize(user))

    def put(self, request):
        serializer = self.get_serializer(instance=request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(first_name=request.data.get('first_name'), last_name=request.data.get('last_name'))
        return Response(self.serialize(user))
