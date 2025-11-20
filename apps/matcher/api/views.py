"""
API views for the AI Resume Hunter application.
"""
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.matcher.models import ResumeData
from apps.matcher.api.serializers import ResumeDataSerializer
from apps.matcher.services.matcher_service import ResumeMatcherService


@api_view(['POST'])
def resume_match_view(request):
    """
    API endpoint to match resumes against job descriptions.
    
    Expected payload:
    {
        "context": "Job description or requirements",
        "category": "resume" or "job_search",
        "threshold": "0.7",
        "noOfMatches": 5,
        "inputPath": "gs://bucket-name"
    }
    """
    serializer = ResumeDataSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Save the request
    serializer.save()
    
    # Process the request through the service layer
    matcher_service = ResumeMatcherService()
    response_data = matcher_service.process_resume_matching(
        serializer.validated_data
    )
    
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def health_check(request):
    """Health check endpoint to verify API is running."""
    return Response({
        'status': 'healthy',
        'message': 'AI Resume Hunter API is running'
    })


@api_view(['GET'])
def stats_view(request):
    """Get statistics about processed resumes."""
    total_requests = ResumeData.objects.count()
    
    return Response({
        'total_requests': total_requests,
        'status': 'success'
    })
