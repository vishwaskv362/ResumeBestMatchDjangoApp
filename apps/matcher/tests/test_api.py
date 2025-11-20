"""
Basic tests for the matcher API.
"""
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status


class HealthCheckTestCase(APITestCase):
    """Test cases for health check endpoint."""
    
    def test_health_check(self):
        """Test that health check endpoint returns 200."""
        response = self.client.get('/api/health/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('status', response.data)
        self.assertEqual(response.data['status'], 'healthy')


class StatsViewTestCase(APITestCase):
    """Test cases for stats endpoint."""
    
    def test_stats_view(self):
        """Test that stats endpoint returns correct structure."""
        response = self.client.get('/api/stats/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_requests', response.data)
        self.assertIn('status', response.data)


class ResumeMatchViewTestCase(APITestCase):
    """Test cases for resume matching endpoint."""
    
    def test_resume_match_invalid_data(self):
        """Test resume match with invalid data returns 400."""
        invalid_data = {
            "context": "Test job description",
            # Missing required fields
        }
        response = self.client.post(
            '/api/match/',
            invalid_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_resume_match_invalid_category(self):
        """Test resume match with invalid category."""
        invalid_data = {
            "context": "Test job description",
            "category": "invalid_category",  # Invalid
            "threshold": "0.7",
            "noOfMatches": 5,
            "inputPath": "gs://test-bucket"
        }
        response = self.client.post(
            '/api/match/',
            invalid_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_resume_match_invalid_threshold(self):
        """Test resume match with invalid threshold."""
        invalid_data = {
            "context": "Test job description",
            "category": "resume",
            "threshold": "1.5",  # Invalid (>1)
            "noOfMatches": 5,
            "inputPath": "gs://test-bucket"
        }
        response = self.client.post(
            '/api/match/',
            invalid_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
