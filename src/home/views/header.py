from rest_framework import viewsets
from src.home.serializers import HeaderSerializer, HeaderIdSerializer
from src.home.models import header
from src.user.permissions.permissions import IsAdminUser, IsAdminOrReadOnly


class HeaderView(viewsets.ModelViewSet):
    queryset = header.objects.all().order_by('id')
    serializer_class = HeaderSerializer

    def get_permissions(self):
        """Set custom permissions for each action."""

        if self.action in ['update', 'partial_update', 'destroy', 'list']:
            self.permission_classes = [IsAdminOrReadOnly, ]

        elif self.action in ['create']:
            self.permission_classes = [IsAdminUser, ]

        return super().get_permissions()

    def get_serializer_class(self):

        if self.action in ['list']:
            self.serializer_class = HeaderIdSerializer

        elif self.action in ['create']:
            self.serializer_class = HeaderSerializer

        return super().get_serializer_class()
