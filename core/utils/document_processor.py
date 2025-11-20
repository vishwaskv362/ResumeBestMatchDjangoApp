"""
Document processing utility for extracting text from various formats.
"""
import io
import docx2txt
from django.conf import settings
from google.cloud import documentai_v1 as documentai


class DocumentProcessor:
    """Processor for extracting text from documents."""
    
    def __init__(self):
        """Initialize Document AI client."""
        self.project_id = settings.GCP_PROJECT_ID
        self.location = settings.GCP_LOCATION
        self.processor_id = settings.GCP_PROCESSOR_ID
        self.client = documentai.DocumentProcessorServiceClient()
    
    def extract_text(self, file_blob) -> str:
        """
        Extract text from a document blob.
        
        Args:
            file_blob: GCS blob object
        
        Returns:
            Extracted text string
        """
        filename = file_blob.name.lower()
        
        try:
            if filename.endswith('.pdf'):
                return self._process_pdf(file_blob)
            elif filename.endswith('.docx'):
                return self._process_docx(file_blob)
            else:
                print(f"Unsupported file format: {filename}")
                return "None"
        except Exception as e:
            print(f"Error extracting text from {filename}: {e}")
            return "None"
    
    def _process_pdf(self, file_blob) -> str:
        """
        Process PDF file using Document AI.
        
        Args:
            file_blob: GCS blob object
        
        Returns:
            Extracted text
        """
        try:
            processor_name = (
                f"projects/{self.project_id}/"
                f"locations/{self.location}/"
                f"processors/{self.processor_id}"
            )
            
            # Download file content
            image_file = io.BytesIO()
            file_blob.download_to_file(image_file)
            
            # Create raw document
            raw_document = documentai.RawDocument(
                content=image_file.getvalue(),
                mime_type="application/pdf"
            )
            
            # Process document
            request = documentai.ProcessRequest(
                name=processor_name,
                raw_document=raw_document
            )
            result = self.client.process_document(request=request)
            
            return result.document.text
            
        except Exception as e:
            print(f"Error processing PDF {file_blob.name}: {e}")
            return "None"
    
    def _process_docx(self, file_blob) -> str:
        """
        Process DOCX file.
        
        Args:
            file_blob: GCS blob object
        
        Returns:
            Extracted text
        """
        try:
            docx_bytes = file_blob.download_as_bytes()
            text = docx2txt.process(io.BytesIO(docx_bytes))
            return text if text else "None"
        except Exception as e:
            print(f"Error processing DOCX {file_blob.name}: {e}")
            return "None"
