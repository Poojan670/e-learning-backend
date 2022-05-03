from rest_framework.generics import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from src.home.models import Languages
from django_filters.rest_framework import DjangoFilterBackend
from src.user.permissions.permissions import IsAdminOrReadOnly


class TutorialsHeaderCreateView(CreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = TutorialsHeader.objects.all()
    serializer_class = TutorialsHeaderSerializer


class TutorialsHeaderListView(ListAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = TutorialsHeader.objects.all()
    serializer_class = TutorialsHeaderSerializer


class TutorialsHeaderDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = TutorialsHeader.objects.all()
    serializer_class = TutorialsHeaderSerializer


class TutorialsCreateView(CreateAPIView):
    permission_classes = [IsAdminOrReadOnly]

    queryset = Tutorial.objects.all()
    serializer_class = TutorialsPageSerializer

    def post(self, request, pk, *args, **kwargs):
        serializer = TutorialsPageSerializer(data=request.data)
        if serializer.is_valid():

            try:
                language = Languages.objects.get(pk=pk)
            except:
                return Response({"error": "Language designaton not found, PLease provide a correct pk"}, status=status.HTTP_400_BAD_REQUEST)
            tutorial = Tutorial(
                title=serializer.data['title'],
                language=language,
            )
            tutorial.save()

            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class TutorialsListView(ListAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Tutorial.objects.all()
    # queryset = Tutorials.objects.filter(language__name__contains="Python")
    serializer_class = TutorialsPageIdSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['language']


class TutorialsDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Tutorial.objects.all()
    serializer_class = TutorialsPageSerializer


class SubTutorialsCreateView(CreateAPIView):
    permission_classes = [IsAdminOrReadOnly]

    queryset = SubTutorial.objects.all()
    serializer_class = SubTutorialsSerializer

    def post(self, request, pk, *args, **kwargs):
        serializer = SubTutorialsSerializer(data=request.data)
        if serializer.is_valid():

            try:
                tutorials = Tutorial.objects.get(pk=pk)
            except:
                return Response({"error": "Language designaton not found, PLease provide a correct pk"}, status=status.HTTP_400_BAD_REQUEST)
            tutorial = SubTutorial(
                sub_tutorial=serializer.data['sub_tutorial'],
                tutorials_title=tutorials,
            )
            tutorial.save()

            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class SubTutorialsListView(ListAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = SubTutorial.objects.all()
    serializer_class = SubTutorialsIdSerializer

    filter_backends = [DjangoFilterBackend]


class SubTutorialsDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = SubTutorial.objects.all()
    serializer_class = SubTutorialsSerializer


class SubTopicsCreateView(CreateAPIView):
    permission_classes = [IsAdminOrReadOnly]

    queryset = SubTopic.objects.all()
    serializer_class = SubTopicsSerializer

    def post(self, request, pk, *args, **kwargs):
        serializer = SubTopicsSerializer(data=request.data)
        if serializer.is_valid():

            try:
                tutorials = SubTutorial.objects.get(pk=pk)
            except:
                return Response({"error": "Language designaton not found, PLease provide a correct pk"}, status=status.HTTP_400_BAD_REQUEST)

            tutorial = SubTopic(
                title=serializer.data['title'],
                description=serializer.data['description'],
                video_title=serializer.data['video_title'],
                video_URL=serializer.data['video_URL'],
                video_description=serializer.data['video_description'],
                video_description_1=serializer.data['video_description_1'],
                topic=tutorials,
            )
            tutorial.save()

            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class SubTopicsListView(ListAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = SubTopic.objects.all()
    serializer_class = SubTopicsIdSerializer


class SubTopicsDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = SubTopic.objects.all()
    serializer_class = SubTopicsSerializer


class SubDetailCreateView(CreateAPIView):
    permission_classes = [IsAdminOrReadOnly]

    queryset = SubDetail.objects.all()
    serializer_class = SubDetailSerializer

    def post(self, request, pk, *args, **kwargs):
        serializer = SubDetailSerializer(data=request.data)
        if serializer.is_valid():

            try:
                tutorials = SubTopic.objects.get(pk=pk)
            except:
                return Response({"error": "Language designaton not found, PLease provide a correct pk"}, status=status.HTTP_400_BAD_REQUEST)
            tutorial = SubDetail(
                title=serializer.data['title'],
                description=serializer.data['description'],
                image=serializer.data['image'],
                relation=tutorials,
            )
            tutorial.save()

            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class SubDetailListView(ListAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = SubDetail.objects.all()
    serializer_class = SubDetailIdSerializer


class SubDetailDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = SubDetail.objects.all()
    serializer_class = SubDetailSerializer
