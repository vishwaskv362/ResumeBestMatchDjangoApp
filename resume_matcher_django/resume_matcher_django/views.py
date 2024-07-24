import io
import os
import uuid

import docx2txt
from django.conf import settings
from google.cloud import storage
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .document_ai import process_document
from .models import DocumentData, ResumeData
from .serializers import ResumeDataSerializer

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(settings.BASE_DIR, "application_default_credentials.json")

credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")


def store_result_in_django_model(filename, extracted_text, filepath, unique_id, confidence_score):
    DocumentData.objects.create(
        unique_id=unique_id,
        filename=filename,
        extracted_text=extracted_text,
        filepath=filepath,
        confidenceScore=confidence_score
    )


def process_bucket_files(validated_data):
    project_id = "wellsfargo-genai24-8032"
    location = "us"
    processor_id = "49c308e26284ad7d"
    unique_id = uuid.uuid4()

    path_to_private_key = os.path.join(settings.BASE_DIR, "creds.json")

    storage_client = storage.Client.from_service_account_json(json_credentials_path=path_to_private_key)

    # storage_client = storage.Client(project='wellsfargo-genai24-8032')

    bucket_name = os.path.basename(validated_data['inputPath'])
    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs()

    for blob in blobs:
        filepath = f"https://storage.googleapis.com/{bucket_name}/{blob.name}"
        if blob.name.endswith('.pdf'):
            extracted_text = process_document(project_id, location, processor_id, blob)
        elif blob.name.endswith('.docx'):
            docx_string = blob.download_as_string()
            extracted_text = docx2txt.process(io.BytesIO(docx_string))
        else:
            continue
        from .vertex_ai import generate
        confidence_score = generate(extracted_text, validated_data['context'], validated_data['category'])
        print(blob.name, filepath, unique_id, confidence_score)
        store_result_in_django_model(blob.name, extracted_text, filepath, unique_id, confidence_score)

    return unique_id


def generate_response(validated_data, unique_id):
    try:
        threshold = validated_data.get('threshold')
        no_of_matches = validated_data.get('noOfMatches')
        document_data = DocumentData.objects.filter(
            unique_id=unique_id,
            confidenceScore__gte=threshold
        ).values('confidenceScore', 'filepath', 'filename').order_by('-confidenceScore')[:no_of_matches]

        results = []
        for data in document_data:
            meta_data_for_each_file = {
                "id": data['filename'],
                "path": data['filepath'],
                "score": data['confidenceScore']
            }
            results.append(meta_data_for_each_file)

        response = {
            "count": len(document_data),
            "metadata": {
                "confidenceScore": threshold
            },
            "results": results,
            "status": "success"
        }
        return response

    except Exception as e:
        response = {
            "count": 0,
            "metadata": {
                "confidenceScore": threshold
            },
            "results": [],
            "status": "error",
            "error_message": str(e)  # Include the error message
        }
        return response


@api_view(['POST'])
def resume_data_view(request):
    if request.method == 'POST':
        serializer = ResumeDataSerializer(data=request.data)
        if serializer.is_valid():
            serialized_data = serializer.validated_data
            uniqueid = process_bucket_files(serialized_data)
            print(f"Unique ID for this request : {uniqueid}")
            serializer.save()
            response = generate_response(validated_data=serialized_data, unique_id=uniqueid)
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def test_api(request):
    total_count = ResumeData.objects.count()
    return Response({'total_count': total_count})


@api_view(['GET'])
def health_check(request):
    """
    A simple health check endpoint.
    """
    from django.http import HttpResponse
    return HttpResponse(content="Alive and kicking!!")
