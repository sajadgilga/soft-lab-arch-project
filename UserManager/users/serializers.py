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

    def update(self, instance, validated_data):
        username = validated_data.get('username', instance.username)
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        if not first_name:
            first_name = instance.first_name
        if not last_name:
            last_name = instance.last_name
        email = validated_data.get('email', instance.email)
        phone = validated_data.get('phone', instance.phone)
        password = validated_data.get('password')

        instance.username = username
        instance.email = email
        instance.phone = phone
        instance.first_name = first_name
        instance.last_name = last_name
        if password:
            instance.set_password(password)
        instance.save()
        return instance
