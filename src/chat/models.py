from django.db import models
from six import python_2_unicode_compatible
from django.utils import timezone
from django.contrib.auth import get_user_model
import uuid
from django.core.exceptions import ValidationError


User = get_user_model()


@python_2_unicode_compatible
class UserChatProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    last_read_date = models.DateTimeField(
        auto_now_add=True,
        blank=False,
        null=False
    )

    online = models.BooleanField(null=False, blank=False, default=False)

    def __str__(self):
        return self.user.full_name

    def read(self):
        self.last_read_date = timezone.now()
        self.save()

    def unread_messages(self):
        return Message.objects.filter(created_at__gt=self.last_read_date).count()


def validate_message_content(content):
    if content is None or content == "" or content.isspace():
        raise ValidationError(
            'Content is empty/invalid',
            code='invalid',
            params={'content': content},
        )


class Message(models.Model):

    id = models.UUIDField(
        primary_key=True,
        null=False,
        default=uuid.uuid4,
        editable=False
    )
    author = models.ForeignKey(UserChatProfile,
                               blank=False,
                               null=False,
                               related_name='author_messages',
                               on_delete=models.CASCADE,
                               )
    content = models.TextField(validators=[validate_message_content])
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    def last_50_messages():
        return Message.objects.order_by('-created_at').all()[:50]
