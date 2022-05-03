from rest_framework import viewsets
from rest_framework import serializers, status
from .models import BillingModel
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser


class BillingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingModel
        fields = '__all__'
        read_only_fields = ('created_at', )


class BillingView(viewsets.GenericViewSet):
    serializer_class = BillingSerializer
    queryset = BillingModel.objects.all().order_by('created_at')

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
