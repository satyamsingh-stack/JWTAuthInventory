from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id', 'username', 'email', 'password']

    def create(self,validated_data):
        validated_data['password']=make_password(validated_data['password'])
        return super().create(validated_data)

class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Inventory
        fields='__all__'
        read_only_fields = ['added_by']