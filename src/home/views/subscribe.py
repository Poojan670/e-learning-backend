from rest_framework import viewsets
from src.home.serializers import SubscribeIdSerializer, SubscribeSerializer
from src.home.models import Subscribe
from src.user.permissions.permissions import IsAdminUser, IsAdminOrReadOnly


class SubscribeView(viewsets.ModelViewSet):
    queryset = Subscribe.objects.all().order_by('id')
    serializer_class = SubscribeSerializer

    def get_permissions(self):
        """Set custom permissions for each action."""

        if self.action in ['update', 'partial_update', 'destroy', 'list']:
            self.permission_classes = [IsAdminOrReadOnly, ]

        elif self.action in ['create']:
            self.permission_classes = [IsAdminUser, ]

        return super().get_permissions()

    def get_serializer_class(self):

        if self.action in ['list']:
            self.serializer_class = SubscribeIdSerializer

        elif self.action in ['create']:
            self.serializer_class = SubscribeSerializer

        return super().get_serializer_class()
