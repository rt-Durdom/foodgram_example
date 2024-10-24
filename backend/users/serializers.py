from users.models import Profile
from rest_framework import serializers


class ProfileSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'avatar', 'is_subscribed')

    def get_is_subscribed(self, profile) -> bool:
        request = self.context.get('request')
        return request.user.is_authenticated and profile.subscribers.filter(id=request.user.id).exists()
