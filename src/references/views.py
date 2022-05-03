from rest_framework.generics import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from src.home.models import Languages
from django_filters.rest_framework import DjangoFilterBackend
from src.user.permissions.permissions import IsAdminOrReadOnly


class ReferencesHeaderCreateView(CreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = ReferencesHeader.objects.all()
    serializer_class = ReferencesHeaderSerializer


class ReferencesHeaderListView(ListAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = ReferencesHeader.objects.all()
    serializer_class = ReferencesHeaderSerializer


class ReferencesHeaderDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = ReferencesHeader.objects.all()
    serializer_class = ReferencesHeaderSerializer


class ReferencesTitleCreateView(CreateAPIView):
    permission_classes = [IsAdminOrReadOnly]

    queryset = ReferencesTitle.objects.all()
    serializer_class = ReferencesTitleSerializer

    def post(self, request, pk, *args, **kwargs):
        serializer = ReferencesTitleSerializer(data=request.data)
        if serializer.is_valid():
            try:
                language = Languages.objects.get(pk=pk)
            except:
                return Response({"error": "Language designaton not found, PLease provide a correct pk"}, status=status.HTTP_400_BAD_REQUEST)
            references = ReferencesTitle(
                title=serializer.data['title'],
                language=language,
            )
            references.save()
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class ReferencesTitleListView(ListAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = ReferencesTitle.objects.all()
    # queryset = Tutorials.objects.filter(language__name__contains="Python")
    serializer_class = ReferencesTitleIdSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['language']


class ReferencesTitleDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = ReferencesTitle.objects.all()
    serializer_class = ReferencesTitleSerializer


class SubReferencesCreateView(CreateAPIView):
    permission_classes = [IsAdminOrReadOnly]

    queryset = SubReferences.objects.all()
    serializer_class = SubReferencesSerializer

    def post(self, request, pk, *args, **kwargs):
        serializer = SubReferencesSerializer(data=request.data)
        if serializer.is_valid():
            try:
                reference = ReferencesTitle.objects.get(pk=pk)
            except:
                return Response({"error": "Language designaton not found, PLease provide a correct pk"}, status=status.HTTP_400_BAD_REQUEST)
            references = SubReferences(
                title=serializer.data['title'],
                description=serializer.data['description'],
                reference_title=reference,
            )
            references.save()
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class SubReferencesListView(ListAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = SubReferences.objects.all()
    serializer_class = SubReferencesIdSerializer

    filter_backends = [DjangoFilterBackend]


class SubReferencesDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = SubReferences.objects.all()
    serializer_class = SubReferencesSerializer


class ReferencesDetailCreateView(CreateAPIView):
    permission_classes = [IsAdminOrReadOnly]

    queryset = ReferencesDetail.objects.all()
    serializer_class = ReferencesDetailSerializer

    def post(self, request, pk, *args, **kwargs):
        serializer = ReferencesDetailSerializer(data=request.data)
        if serializer.is_valid():
            try:
                reference = SubReferences.objects.get(pk=pk)
            except:
                return Response({"error": "Language designaton not found, PLease provide a correct pk"}, status=status.HTTP_400_BAD_REQUEST)
            references = ReferencesDetail(
                title=serializer.data['title'],
                description=serializer.data['description'],
                sub_references=reference,
            )
            references.save()
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class ReferencesDetailListView(ListAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = ReferencesDetail.objects.all()
    serializer_class = ReferencesDetailIdSerializer


class ReferencesDetailDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = ReferencesDetail.objects.all()
    serializer_class = ReferencesDetailSerializer


class ReferencesDetailLanguageListView(ListAPIView):
    permission_classes = [IsAdminOrReadOnly]

    queryset = ReferencesDetail.objects.all()
    serializer_class = ReferencesDetailIdSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['sub_references']
