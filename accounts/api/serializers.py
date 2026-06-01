from rest_framework import serializers
from decouple import config

from accounts.models import User

class UserSerializer(serializers.ModelSerializer):
    '''Serializer for the User model'''

    department_name=serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'department', 'password', 'department_name']
        extra_kwargs = {
            'password': {'write_only': True},
            'department': {'write_only': True},
            'email': {'read_only': True},
        }

    def get_department_name(self, obj):
        '''Return the name of the department for the user'''

        return obj.department.name if obj.department else None
    
    def create(self, validated_data):
        '''Create and return a new user'''

        username = validated_data.get('username')
        domain = config('ORG_DOMAIN')
        if not validated_data.get('email'):
            validated_data['email'] = f"{username}@{domain}"

        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        '''Update and return an existing user'''

        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
    