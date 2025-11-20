"""
Admin configuration for matcher app.
"""
from django.contrib import admin
from .models import ResumeData, DocumentData


@admin.register(ResumeData)
class ResumeDataAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'threshold', 'noOfMatches', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['context', 'inputPath']
    readonly_fields = ['created_at']


@admin.register(DocumentData)
class DocumentDataAdmin(admin.ModelAdmin):
    list_display = ['filename', 'unique_id', 'confidenceScore', 'created_at']
    list_filter = ['created_at']
    search_fields = ['filename', 'unique_id', 'extracted_text']
    readonly_fields = ['created_at']
