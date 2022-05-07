from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from src.user.tasks.tasks import subscribed_mail
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAdminUser


def send_emails(data):
    try:
        email = data['data']
        length = len(email)
        if length == 0:
            raise ValidationError("Email List is Empty",
                                  status=status.HTTP_400_BAD_REQUEST)
        try:
            for i in range(0, length):
                subscribed_mail.delay(email[i])
                print("Hello")
            print("Email Sent!")
        except Exception as e:
            print(str(e))

    except Exception as e:
        print(str(e))
        print("Unable to send emails")


class SendEmailsView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, format=None):
        try:
            r = requests.post("http://127.0.0.1:8001/api/v1/send/mail/")
        except:
            return Response({"msg": "Error Occured, Couldn't fetch from the given url"})
        if r.status_code == 200:
            data = r.json()
        else:
            return Response({"msg": "Bad Request, Please Try Again!"})

        try:
            send_emails(data)
        except Exception as e:
            return Response({"error": "Error occured due to {}".format(str(e))},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response("Emails Sent", status=status.HTTP_200_OK)
