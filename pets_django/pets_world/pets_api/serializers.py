from rest_framework import serializers
from .models import *

class UserDataSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = '__all__'

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class UserLoginSerializers(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class PetsDataSerializers(serializers.ModelSerializer):
    class Meta:
        model = PetsData
        fields = '__all__'