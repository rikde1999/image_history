# Model serializers
"""
from rest_framework import serializers
from .models import User, Interaction

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'mobile_number', 'name', 'is_verified']

class InteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interaction
        fields = ['id', 'user', 'image_name', 'action', 'timestamp']

class OTPVerificationSerializer(serializers.Serializer):
    mobile_number = serializers.CharField()
    otp = serializers.CharField()
    name = serializers.CharField(required=False)

class ImageInteractionSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    image_name = serializers.CharField()
    action = serializers.CharField()
"""

# Use of custom serializer
from rest_framework import serializers
from .models import User, Interaction
from image_app.constants import USER_CHOICES


class UserSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    mobile_number = serializers.CharField(max_length=15)
    name = serializers.CharField(max_length=100, allow_blank=True, required=False)
    is_verified = serializers.BooleanField(default=False)

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.mobile_number = validated_data.get(
            "mobile_number", instance.mobile_number
        )
        instance.name = validated_data.get("name", instance.name)
        instance.is_verified = validated_data.get("is_verified", instance.is_verified)
        instance.save()
        return instance


class InteractionSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=50)
    image_name = serializers.CharField(max_length=50)
    action = serializers.ChoiceField(choices=USER_CHOICES)
    timestamp = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Interaction.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.user = validated_data.get("user_id", instance.user)
        instance.image_name = validated_data.get("image_name", instance.image_name)
        instance.action = validated_data.get("action", instance.action)
        instance.save()
        return instance


class OTPVerificationSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=15)
    otp = serializers.CharField(max_length=6)
    name = serializers.CharField(max_length=100, required=False)
