from rest_framework.response import Response
from rest_framework.views import APIView
from src.user.permissions.permissions import IsAdminUser
from src.home.models import Subscribe


class SendEmailView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, format=None):
        emails = Subscribe.objects.all().values_list('email', flat=True)

        data = list(emails)

        if emails is not None:
            return Response({"data": data})
        elif emails is None:
            return Response({"data": ""})
        else:
            return Response({"data": ""})


# class SendEmailView(CreateAPIView):

#     queryset = EmailSend.objects.all()
#     serializer_class = SendMailSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = SendMailSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             email = serializer.data['sub']
#             length = len(email)
#             dat = []
#             for i in range(0, length):
#                 obj = Subscribe.objects.get(id=email[i])
#                 dat.append(obj.email)

#             return Response({
#                 "data": dat
#             }, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
