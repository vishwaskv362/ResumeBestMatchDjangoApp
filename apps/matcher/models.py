"""
Models for the resume matcher application.
"""
import uuid
from django.db import models


class ResumeData(models.Model):
    """Model to store resume matching request data."""
    id = models.AutoField(primary_key=True)
    context = models.TextField(help_text="Job description or requirements")
    category = models.CharField(max_length=100, help_text="Category: 'resume' or 'job_search'")
    threshold = models.TextField(help_text="Minimum confidence score threshold")
    noOfMatches = models.IntegerField(help_text="Number of top matches to return")
    inputPath = models.URLField(help_text="GCS bucket path with resumes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'resume_data'
        verbose_name = 'Resume Data'
        verbose_name_plural = 'Resume Data'
        ordering = ['-created_at']

    def __str__(self):
        return f"Request {self.id} - {self.category}"


class DocumentData(models.Model):
    """Model to store extracted document data and match scores."""
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    filename = models.CharField(max_length=255)
    extracted_text = models.TextField(default="Text Empty in exception cases")
    filepath = models.CharField(max_length=255)
    confidenceScore = models.CharField(max_length=10, default="0")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'document_data'
        verbose_name = 'Document Data'
        verbose_name_plural = 'Document Data'
        ordering = ['-confidenceScore', '-created_at']
        indexes = [
            models.Index(fields=['unique_id', 'confidenceScore']),
        ]

    def __str__(self):
        return f"{self.filename} - Score: {self.confidenceScore}"
