from .models import Comment, Reply
from .comments_serializer import CommentSerializer, ReplySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


class ReplyList(APIView):
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ['user', 'user__email', 'user__full_name']
    filter_fields = ['user__full_name', 'user__email']
    ordering_fields = ['reply_at', 'id']

    def get(self, request):
        reply = Reply.objects.all()
        serializer = ReplySerializer(reply, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReplySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReplyDetail(APIView):

    def get_object(self, comment):
        try:
            return Reply.objects.filter(comment=comment)
        except Comment.DoesNotExist:
            raise Http404

    def get(self, request, comment):
        reply = self.get_object(comment)
        serializer = ReplySerializer(reply, many=True)
        return Response(serializer.data)

    def put(self, request, comment):
        reply = self.get_object(comment)
        serializer = ReplySerializer(reply, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, comment):
        reply = self.get_object(comment)
        reply.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentList(APIView):

    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ['user', 'user__email', 'user__full_name']
    filter_fields = ['user__full_name', 'user__email']
    ordering_fields = ['comment_at', 'id']

    def get(self, request):
        comment = Comment.objects.all()
        serializer = CommentSerializer(comment, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetail(APIView):

    def get_object(self, comment_id):
        try:
            return Comment.objects.get(comment_id=comment_id)
        except Comment.DoesNotExist:
            raise Http404

    def get(self, request, comment_id):
        comment = self.get_object(comment_id)
        serializer = CommentSerializer(comment, many=True)
        return Response(serializer.data)

    def put(self, request, comment_id):
        comment = self.get_object(comment_id)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, comment_id):
        comment = self.get_object(comment_id)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentLike(APIView):

    def get_object(self, pk, comment_id):
        try:
            return Comment.objects.get(pk=pk, comment_id=comment_id)
        except Comment.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        comment = self.get_object(pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def patch(self, request, pk, comment_id):
        comment = self.get_object(pk, comment_id=comment_id)
        data = {"likes": comment.likes + int(1)}
        serializer = CommentSerializer(comment, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDislike(APIView):

    def get_object(self, comment_id, pk):
        try:
            return Comment.objects.get(comment_id=comment_id, pk=pk)
        except Comment.DoesNotExist:
            raise Http404

    def get(self, request, comment_id):
        comment = self.get_object(comment_id)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def patch(self, request, comment_id, pk):
        comment = self.get_object(comment_id, pk=pk)
        data = {"dislikes": comment.dislikes + int(1)}
        serializer = CommentSerializer(comment, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
