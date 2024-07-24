import uuid

from django.db import models


class ResumeData(models.Model):
    id = models.AutoField(primary_key=True)
    context = models.TextField()
    category = models.CharField(max_length=100)
    threshold = models.TextField()
    noOfMatches = models.IntegerField()
    inputPath = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)


class DocumentData(models.Model):
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False)
    filename = models.CharField(max_length=255)
    extracted_text = models.TextField(default="Text Empty in exception cases")
    filepath = models.CharField(max_length=255)
    confidenceScore = models.CharField(max_length=10, default="0")
