"""
Tests for the matcher models.
"""
from django.test import TestCase
from apps.matcher.models import ResumeData, DocumentData
import uuid


class ResumeDataModelTestCase(TestCase):
    """Test cases for ResumeData model."""
    
    def test_create_resume_data(self):
        """Test creating a ResumeData instance."""
        resume_data = ResumeData.objects.create(
            context="Test job description",
            category="resume",
            threshold="0.7",
            noOfMatches=5,
            inputPath="gs://test-bucket"
        )
        
        self.assertIsNotNone(resume_data.id)
        self.assertEqual(resume_data.context, "Test job description")
        self.assertEqual(resume_data.category, "resume")
        self.assertEqual(resume_data.threshold, "0.7")
        self.assertEqual(resume_data.noOfMatches, 5)
    
    def test_resume_data_str(self):
        """Test string representation of ResumeData."""
        resume_data = ResumeData.objects.create(
            context="Test",
            category="resume",
            threshold="0.7",
            noOfMatches=5,
            inputPath="gs://test"
        )
        expected_str = f"Request {resume_data.id} - resume"
        self.assertEqual(str(resume_data), expected_str)


class DocumentDataModelTestCase(TestCase):
    """Test cases for DocumentData model."""
    
    def test_create_document_data(self):
        """Test creating a DocumentData instance."""
        test_uuid = uuid.uuid4()
        doc_data = DocumentData.objects.create(
            unique_id=test_uuid,
            filename="test_resume.pdf",
            extracted_text="Test extracted text",
            filepath="https://storage.googleapis.com/bucket/test.pdf",
            confidenceScore="0.85"
        )
        
        self.assertEqual(doc_data.unique_id, test_uuid)
        self.assertEqual(doc_data.filename, "test_resume.pdf")
        self.assertEqual(doc_data.confidenceScore, "0.85")
    
    def test_document_data_default_values(self):
        """Test default values for DocumentData."""
        doc_data = DocumentData.objects.create(
            filename="test.pdf",
            filepath="http://test.com/test.pdf"
        )
        
        self.assertIsNotNone(doc_data.unique_id)
        self.assertEqual(doc_data.extracted_text, "Text Empty in exception cases")
        self.assertEqual(doc_data.confidenceScore, "0")
    
    def test_document_data_str(self):
        """Test string representation of DocumentData."""
        doc_data = DocumentData.objects.create(
            filename="resume.pdf",
            filepath="http://test.com",
            confidenceScore="0.9"
        )
        expected_str = "resume.pdf - Score: 0.9"
        self.assertEqual(str(doc_data), expected_str)
