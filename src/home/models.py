from django.db import models


class header(models.Model):

    title = models.CharField(max_length=200)
    description = models.TextField(max_length=300)
    sub_title = models.CharField(max_length=100, blank=True, null=True)
    side_image = models.ImageField(upload_to="home")

    def __str__(self):
        return self.title


class Subscribe(models.Model):

    email = models.EmailField(
        unique=True, null=False, blank=False, help_text="Enter Email Address*")

    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class BodyHeader(models.Model):
    title = models.CharField(max_length=255, blank=False, null=True)

    video_url = models.URLField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Body(models.Model):

    icon = models.ImageField(upload_to="body")
    sub_title = models.CharField(
        max_length=100, help_text="Programming Made Easy")
    description = models.TextField()

    relation = models.ForeignKey(
        BodyHeader, on_delete=models.CASCADE, related_name="realation")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sub_title


class Languages(models.Model):

    icon = models.ImageField(upload_to="languages")

    name = models.CharField(max_length=100, blank=False,
                            null=False, help_text="Python,Java....", unique=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
