from rest_framework import viewsets
from src.home.serializers import BodySerializer, BodyIdSerializer
from src.home.models import Body
from src.user.permissions.permissions import IsAdminUser, IsAdminOrReadOnly


class BodyView(viewsets.ModelViewSet):
    queryset = Body.objects.all().order_by('created_at')
    serializer_class = BodySerializer

    def get_permissions(self):
        """Set custom permissions for each action."""

        if self.action in ['update', 'partial_update', 'destroy', 'list']:
            self.permission_classes = [IsAdminOrReadOnly, ]

        elif self.action in ['create']:
            self.permission_classes = [IsAdminUser, ]

        return super().get_permissions()

    def get_serializer_class(self):

        if self.action in ['list']:
            self.serializer_class = BodyIdSerializer

        elif self.action in ['create']:
            self.serializer_class = BodySerializer

        return super().get_serializer_class()
