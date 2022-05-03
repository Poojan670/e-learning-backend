from django.db import models
from src.home.models import Languages


class TutorialsHeader(models.Model):
    language = models.OneToOneField(
        Languages, on_delete=models.CASCADE, related_name="tutorials_header")

    title = models.CharField(max_length=300, null=False, blank=False)
    description1 = models.TextField(null=False, blank=False)
    description2 = models.TextField(null=False, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Tutorial(models.Model):

    # Introduction, Flow Control, Function ,Data Types ...
    title = models.CharField(max_length=200, null=False, blank=False)

    language = models.ForeignKey(
        Languages, on_delete=models.CASCADE, related_name="tutorial_language")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class SubTutorial(models.Model):

    # Getting Started, Keyword and Identifiers......
    sub_tutorial = models.CharField(max_length=200, null=True, blank=True)

    tutorials_title = models.ForeignKey(
        Tutorial, on_delete=models.CASCADE, related_name="sub_tutorials")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.sub_tutorial


class SubTopic(models.Model):

    topic = models.ForeignKey(
        SubTutorial, on_delete=models.CASCADE, related_name="subtopics")

    # How to Get Started With Python?
    title = models.CharField(max_length=200)
    description = models.TextField()

    # Video: Introduction to Python
    video_title = models.CharField(max_length=200, blank=True, null=True)
    video_URL = models.URLField(blank=True, null=True)
    video_description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class SubDetail(models.Model):

    # The Easiest Way to Run Python
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="tutorials")

    relation = models.ForeignKey(
        SubTopic, on_delete=models.CASCADE, related_name="sub_desc", null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
