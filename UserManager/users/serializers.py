from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'password', 'last_name', 'username', 'email', 'phone', 'role']
        read_only_fields = ['id', 'first_name', 'last_name', 'role']

    def get_role(self, obj):
        if obj.is_superuser:
            return 'admin'
        return obj.get_role_display()

    def create(self, validated_data):
        username, email, phone, password = validated_data['username'], validated_data['email'], validated_data['phone'], \
                                           validated_data['password']
        user = User.objects.create(username=username, email=email, phone=phone, role=User.Roles.CLIENT)
        user.set_password(password)
        user.save()
        return user
