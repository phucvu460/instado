from rest_framework.viewsets import ModelViewSet
from accounts.models import User, Profile
from accounts.serializers import UserSerializer, FriendListSerializer
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.response import Response




class UserModelViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    allowed_methods = ('GET', 'HEAD', 'OPTIONS')
    pagination_class = None  # Get all user

    def list(self, request, *args, **kwargs):
        # Get all friends except yourself
        self.queryset = self.queryset.exclude(id=request.user.id)
        return super(UserModelViewSet, self).list(request, *args, **kwargs)


class FriendListViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = FriendListSerializer
    allowed_methods = ('GET', 'HEAD', 'OPTIONS')
    pagination_class = None

    def list(self, request, *args, **kwargs):
        qs = self.queryset.filter(Q(user=request.user))
        profile = get_object_or_404(qs)
        # self.queryset = profile.friends.all()
        serializer = self.serializer_class(instance=profile)

        return Response(serializer.data)