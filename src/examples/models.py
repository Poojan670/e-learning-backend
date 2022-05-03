from django.db import models
from src.home.models import Languages


class ExamplesHeader(models.Model):
    language = models.OneToOneField(
        Languages, on_delete=models.CASCADE, related_name="examples_header")

    title = models.CharField(max_length=300)
    description1 = models.TextField()
    description2 = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ExampleCategory(models.Model):

    # Advanced, Introduction, Object Oriented ,Decision Making ...
    title = models.CharField(max_length=200, null=False, blank=False)

    language = models.ForeignKey(
        Languages, on_delete=models.CASCADE, related_name="example_language")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ExampleTitle(models.Model):

    # Python Program to Print Hello world!, Python Program to Add Two Numbers......
    title = models.CharField(max_length=200, null=True, blank=True)

    example_category = models.ForeignKey(
        ExampleCategory, on_delete=models.CASCADE, related_name="example_title")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_popular = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class ExampleDetail(models.Model):

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="tutorials")

    relation = models.ForeignKey(
        ExampleTitle, on_delete=models.CASCADE, related_name="example_detail", null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
