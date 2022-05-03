from rest_framework import viewsets, serializers
from rest_framework.response import Response
from rest_framework import status
from .models import Blog
from src.user.permissions.permissions import IsAdminUser, IsAdminOrReadOnly


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'
        extra_kwargs = {
            'created_on': {'read_only': True},
            'status': {'read_only': True},
        }


class BlogView(viewsets.GenericViewSet):
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return self.get_paginated_response(self.paginate_queryset(serializer.data))

    def retrieve(self, request, pk):
        item = self.get_object()
        serializer = self.get_serializer(item)
        return Response(serializer.data)

    def destroy(self, request):
        item = self.get_object()
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        """Set custom permissions for each action."""

        if self.action in ['update', 'partial_update', 'destroy', 'list']:
            self.permission_classes = [IsAdminOrReadOnly, ]

        elif self.action in ['create']:
            self.permission_classes = [IsAdminUser, ]

        return super().get_permissions()
