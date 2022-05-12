from django.db import models
from cloudinary.models import CloudinaryField
from django.dispatch import receiver
from django.db.models import signals
from django.db.models.signals import pre_delete
import cloudinary.uploader
from src.core.models import CoreModel


class header(CoreModel):

    title = models.CharField(max_length=200)
    description = models.TextField(max_length=300)
    sub_title = models.CharField(max_length=100, blank=True, null=True)
    side_image = models.ImageField(upload_to="home")

    def __str__(self):
        return self.title


@receiver(pre_delete, sender=header)
def photo_delete(sender, instance, **kwargs):
    cloudinary.uploader.destroy(instance.side_image.file_name)
    instance.delete()
    # cloudinary.uploader.destroy(instance.side_image)


class Subscribe(CoreModel):

    email = models.EmailField(
        unique=True, null=False, blank=False, help_text="Enter Email Address*")

    def __str__(self):
        return self.email


class BodyHeader(CoreModel):
    title = models.CharField(max_length=255, blank=False, null=True)

    video_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title


class Body(CoreModel):

    icon = models.ImageField(upload_to="body")
    sub_title = models.CharField(
        max_length=100, help_text="Programming Made Easy")
    description = models.TextField()

    relation = models.ForeignKey(
        BodyHeader, on_delete=models.CASCADE, related_name="realation")

    def __str__(self):
        return self.sub_title


class Languages(CoreModel):

    icon = models.ImageField(upload_to="languages")

    name = models.CharField(max_length=100, blank=False,
                            null=False, help_text="Python,Java....", unique=True)

    def __str__(self):
        return self.name
