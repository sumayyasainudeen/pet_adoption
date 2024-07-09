from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
CustomUser = get_user_model()

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

class PetDetailsSerializers(serializers.ModelSerializer):

    donor_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(), source='donor', write_only=True
    )
    donor = UserSerializers(read_only=True)

    class Meta:
        model = PetDetails
        fields = '__all__'
        extra_kwargs = {
            'donor': {'required': False}
        }

class AdoptedPetsSerializers(serializers.ModelSerializer):

    pet_id = serializers.PrimaryKeyRelatedField(
        queryset=PetDetails.objects.all(), source='pet', write_only=True
    )

    pet = PetDetailsSerializers(read_only=True)
    
    class Meta:
        model = AdoptedPets
        fields = '__all__'

class AdoptionNotificationSerializers(serializers.ModelSerializer):

    user_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(), source='user', write_only=True
    )
    user = UserSerializers(read_only=True)
    pet = PetDetailsSerializers(read_only=True)

    class Meta:
        model = AdoptionNotification
        fields = '__all__'