"""
Service layer for resume matching business logic.
"""
import uuid
from typing import Dict, List, Any

from apps.matcher.models import DocumentData
from core.utils.gcp_storage import GCPStorageHandler
from core.utils.document_processor import DocumentProcessor
from core.utils.ai_matcher import AIMatcherService


class ResumeMatcherService:
    """Service to handle resume matching operations."""
    
    def __init__(self):
        self.storage_handler = GCPStorageHandler()
        self.document_processor = DocumentProcessor()
        self.ai_matcher = AIMatcherService()
    
    def process_resume_matching(self, validated_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main method to process resume matching request.
        
        Args:
            validated_data: Validated request data containing job description, 
                          threshold, category, etc.
        
        Returns:
            Dict containing match results
        """
        try:
            # Generate unique ID for this request
            unique_id = uuid.uuid4()
            
            # Process files from GCS bucket
            self._process_bucket_files(validated_data, unique_id)
            
            # Generate and return response
            response = self._generate_response(validated_data, unique_id)
            return response
            
        except Exception as e:
            return {
                "count": 0,
                "metadata": {
                    "confidenceScore": validated_data.get('threshold', '0')
                },
                "results": [],
                "status": "error",
                "error_message": str(e)
            }
    
    def _process_bucket_files(
        self, 
        validated_data: Dict[str, Any], 
        unique_id: uuid.UUID
    ) -> None:
        """
        Process all files in the specified GCS bucket.
        
        Args:
            validated_data: Request data
            unique_id: Unique identifier for this request
        """
        bucket_path = validated_data['inputPath']
        job_description = validated_data['context']
        category = validated_data['category']
        
        # List all files in the bucket
        files = self.storage_handler.list_bucket_files(bucket_path)
        
        for file_blob in files:
            try:
                # Extract text from document
                extracted_text = self.document_processor.extract_text(file_blob)
                
                if not extracted_text or extracted_text == "None":
                    continue
                
                # Get AI match score
                confidence_score = self.ai_matcher.calculate_match_score(
                    extracted_text, 
                    job_description, 
                    category
                )
                
                # Store result in database
                self._store_document_data(
                    filename=file_blob.name,
                    extracted_text=extracted_text,
                    filepath=self.storage_handler.get_file_url(
                        file_blob.bucket.name, 
                        file_blob.name
                    ),
                    unique_id=unique_id,
                    confidence_score=confidence_score
                )
                
            except Exception as e:
                print(f"Error processing file {file_blob.name}: {e}")
                continue
    
    def _store_document_data(
        self,
        filename: str,
        extracted_text: str,
        filepath: str,
        unique_id: uuid.UUID,
        confidence_score: str
    ) -> None:
        """Store processed document data in database."""
        DocumentData.objects.create(
            unique_id=unique_id,
            filename=filename,
            extracted_text=extracted_text,
            filepath=filepath,
            confidenceScore=confidence_score
        )
    
    def _generate_response(
        self, 
        validated_data: Dict[str, Any], 
        unique_id: uuid.UUID
    ) -> Dict[str, Any]:
        """
        Generate response with top matching resumes.
        
        Args:
            validated_data: Request data
            unique_id: Unique identifier for this request
        
        Returns:
            Response dictionary with matches
        """
        threshold = float(validated_data.get('threshold', 0))
        no_of_matches = validated_data.get('noOfMatches', 10)
        
        # Query documents above threshold
        document_data = DocumentData.objects.filter(
            unique_id=unique_id,
            confidenceScore__gte=str(threshold)
        ).values(
            'confidenceScore', 
            'filepath', 
            'filename'
        ).order_by('-confidenceScore')[:no_of_matches]
        
        # Format results
        results = [
            {
                "id": data['filename'],
                "path": data['filepath'],
                "score": data['confidenceScore']
            }
            for data in document_data
        ]
        
        return {
            "count": len(results),
            "metadata": {
                "confidenceScore": threshold
            },
            "results": results,
            "status": "success"
        }
