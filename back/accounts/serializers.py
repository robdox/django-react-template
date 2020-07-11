from rest_framework import serializers

from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        instance.email = validated_data.get("email", instance.email)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
        )
