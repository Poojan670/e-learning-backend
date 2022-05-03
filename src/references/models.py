from django.db import models
from src.home.models import Languages


class ReferencesHeader(models.Model):

    title = models.CharField(max_length=100, null=False, blank=False)

    language = models.OneToOneField(
        Languages, on_delete=models.CASCADE, related_name="references_language")

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now_add=True)


class ReferencesTitle(models.Model):

    title = models.CharField(max_length=200, null=False, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now_add=True)

    language = models.ForeignKey(
        Languages, on_delete=models.CASCADE, related_name="references_title")


class SubReferences(models.Model):

    title = models.CharField(max_length=100, null=False, blank=False)

    description = models.TextField(blank=True, null=True)

    reference_title = models.ForeignKey(
        ReferencesTitle, on_delete=models.CASCADE, related_name="sub_references")

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now_add=True)


class ReferencesDetail(models.Model):

    title = models.CharField(max_length=100, null=True, blank=True)

    description = models.TextField(blank=True, null=True)

    sub_references = models.ForeignKey(
        SubReferences, related_name="references_detail", on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now_add=True)
