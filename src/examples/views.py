from rest_framework.generics import *
from src.examples.serializers import (
    ExamplesHeaderSerializer, ExampleCategorySerializer, ExampleCategoryIdSerializer,
    ExampleTitleSerializer, ExampleTitleIdSerializer, ExampleDetailSerializer, ExampleDetailIdSerializer
)
from .models import (ExamplesHeader, ExampleTitle,
                     ExampleCategory, ExampleDetail)

from rest_framework.response import Response
from rest_framework import status
from src.home.models import Languages
from django_filters.rest_framework import DjangoFilterBackend
from src.user.permissions.permissions import IsAdminOrReadOnly


class ExamplesHeaderCreateView(CreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = ExamplesHeader.objects.all()
    serializer_class = ExamplesHeaderSerializer


class ExamplesHeaderListView(ListAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = ExamplesHeader.objects.all()
    serializer_class = ExamplesHeaderSerializer


class ExamplesHeaderDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = ExamplesHeader.objects.all()
    serializer_class = ExamplesHeaderSerializer


class ExampleCategoryCreateView(CreateAPIView):
    permission_classes = [IsAdminOrReadOnly]

    queryset = ExampleCategory.objects.all()
    serializer_class = ExampleCategorySerializer

    def post(self, request, pk, *args, **kwargs):
        serializer = ExampleCategorySerializer(data=request.data)
        if serializer.is_valid():

            try:
                language = Languages.objects.get(pk=pk)
            except:
                return Response({"error": "Language designaton not found, PLease provide a correct pk"}, status=status.HTTP_400_BAD_REQUEST)

            examples = ExampleCategory(
                title=serializer.data['title'],
                language=language,
            )
            examples.save()

            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class ExampleCategoryListView(ListAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = ExampleCategory.objects.all()
    serializer_class = ExampleCategoryIdSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['language']


class ExampleCategoryDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = ExampleCategory.objects.all()
    serializer_class = ExampleCategorySerializer


class ExampleTitleCreateView(CreateAPIView):
    permission_classes = [IsAdminOrReadOnly]

    queryset = ExampleTitle.objects.all()
    serializer_class = ExampleTitleSerializer

    def post(self, request, pk, *args, **kwargs):
        serializer = ExampleTitleSerializer(data=request.data)
        if serializer.is_valid():
            try:
                example = ExampleTitle.objects.get(pk=pk)
            except:
                return Response({"error": "Language designaton not found, PLease provide a correct pk"}, status=status.HTTP_400_BAD_REQUEST)
            examples = ExampleTitle(
                sub_tutorial=serializer.data['sub_tutorial'],
                tutorials_title=example,
            )
            examples.save()
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class ExampleTitleListView(ListAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = ExampleTitle.objects.all()
    serializer_class = ExampleTitleIdSerializer

    filter_backends = [DjangoFilterBackend]


class ExampleTitleDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = ExampleTitle.objects.all()
    serializer_class = ExampleTitleSerializer


class ExampleDetailCreateView(CreateAPIView):
    permission_classes = [IsAdminOrReadOnly]

    queryset = ExampleDetail.objects.all()
    serializer_class = ExampleDetailSerializer

    def post(self, request, pk, *args, **kwargs):
        serializer = ExampleDetailSerializer(data=request.data)
        if serializer.is_valid():
            try:
                example = ExampleDetail.objects.get(pk=pk)
            except:
                return Response({"error": "Language designaton not found, PLease provide a correct pk"}, status=status.HTTP_400_BAD_REQUEST)
            examples = ExampleDetail(
                title=serializer.data['title'],
                description=serializer.data['description'],
                image=serializer.data['image'],
                relation=example,
            )
            examples.save()
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class ExampleDetailListView(ListAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = ExampleDetail.objects.all()
    serializer_class = ExampleDetailIdSerializer


class ExampleDetailDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = ExampleDetail.objects.all()
    serializer_class = ExampleDetailSerializer


class PopularExamples(ListAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = ExampleTitle.objects.filter(is_popular=True)
    serializer_class = ExampleTitleIdSerializer
