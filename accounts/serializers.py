from accounts.models import User, Profile
from rest_framework.serializers import ModelSerializer, CharField


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


class ProfileSerializer(ModelSerializer):
    user = CharField(source='user.username')

    class Meta:
        model = Profile
        fields = ['user', 'bio', 'slug']


class FriendListSerializer(ModelSerializer):
    friends = ProfileSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = ['friends']
