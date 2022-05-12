from .models import Reviews, ReviewsReply
from .reviews_serializer import ReviewsSerializer, ReviewsReplySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


class ReviewReplyList(APIView):
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ['user', 'user__email', 'user__full_name']
    filter_fields = ['user__full_name', 'user__email']
    ordering_fields = ['reply_at', 'id']

    def get(self, request):
        reply = ReviewsReply.objects.all()
        serializer = ReviewsReplySerializer(reply, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReviewsReplySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewsReplyDetail(APIView):

    def get_object(self, review):
        try:
            return ReviewsReply.objects.filter(review=review)
        except ReviewsReply.DoesNotExist:
            raise Http404

    def get(self, request, review):
        reply = self.get_object(review)
        serializer = ReviewsReply(reply, many=True)
        return Response(serializer.data)

    def put(self, request, review):
        reply = self.get_object(review)
        serializer = ReviewsReply(reply, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, review):
        reply = self.get_object(review)
        reply.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewsList(APIView):

    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ['user', 'user__email', 'user__full_name']
    filter_fields = ['user__full_name', 'user__email']
    ordering_fields = ['reviewed_at', 'id']

    def get(self, request):
        review = Reviews.objects.all()
        serializer = ReviewsSerializer(review, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReviewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewDetail(APIView):

    def get_object(self, review_id):
        try:
            return Reviews.objects.get(review_id=review_id)
        except Reviews.DoesNotExist:
            raise Http404

    def get(self, request, review_id):
        review = self.get_object(review_id)
        serializer = ReviewsSerializer(review, many=True)
        return Response(serializer.data)

    def put(self, request, review_id):
        review = self.get_object(review_id)
        serializer = ReviewsSerializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, review_id):
        review = self.get_object(review_id)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewLike(APIView):

    def get_object(self, pk, review_id):
        try:
            return Reviews.objects.get(pk=pk, review_id=review_id)
        except Reviews.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        review = self.get_object(pk)
        serializer = ReviewsSerializer(review)
        return Response(serializer.data)

    def patch(self, request, pk, review_id):
        review = self.get_object(pk, review_id=review_id)
        data = {"likes": review.likes + int(1)}
        serializer = ReviewsSerializer(review, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewDislike(APIView):

    def get_object(self, review_id, pk):
        try:
            return Reviews.objects.get(review_id=review_id, pk=pk)
        except Reviews.DoesNotExist:
            raise Http404

    def get(self, request, review_id):
        review = self.get_object(review_id)
        serializer = ReviewsSerializer(review)
        return Response(serializer.data)

    def patch(self, request, review_id, pk):
        review = self.get_object(review_id, pk=pk)
        data = {"dislikes": review.dislikes + int(1)}
        serializer = ReviewsSerializer(review, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
