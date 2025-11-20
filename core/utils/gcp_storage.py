"""
Google Cloud Storage handler utility.
"""
import os
from typing import List
from django.conf import settings
from google.cloud import storage


class GCPStorageHandler:
    """Handler for Google Cloud Storage operations."""
    
    def __init__(self):
        """Initialize GCS client with credentials."""
        self.credentials_path = settings.GOOGLE_APPLICATION_CREDENTIALS
        
        # Check if using service account key file
        if os.path.exists(os.path.join(settings.BASE_DIR, "creds.json")):
            path_to_private_key = os.path.join(settings.BASE_DIR, "creds.json")
            self.client = storage.Client.from_service_account_json(
                json_credentials_path=path_to_private_key
            )
        else:
            # Use application default credentials
            self.client = storage.Client(project=settings.GCP_PROJECT_ID)
    
    def list_bucket_files(self, bucket_path: str) -> List:
        """
        List all files in a GCS bucket.
        
        Args:
            bucket_path: GCS bucket path (gs://bucket-name or just bucket-name)
        
        Returns:
            List of blob objects
        """
        # Extract bucket name from path
        bucket_name = bucket_path.replace('gs://', '').split('/')[0]
        bucket = self.client.bucket(bucket_name)
        
        # List all blobs
        blobs = list(bucket.list_blobs())
        return blobs
    
    def get_file_url(self, bucket_name: str, blob_name: str) -> str:
        """
        Generate public URL for a file.
        
        Args:
            bucket_name: Name of the bucket
            blob_name: Name of the blob/file
        
        Returns:
            Public URL string
        """
        return f"https://storage.googleapis.com/{bucket_name}/{blob_name}"
    
    def download_file(self, blob) -> bytes:
        """
        Download file content as bytes.
        
        Args:
            blob: GCS blob object
        
        Returns:
            File content as bytes
        """
        return blob.download_as_bytes()
