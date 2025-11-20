"""
AI-powered resume matching utility using Google Vertex AI.
"""
import vertexai
import vertexai.preview.generative_models as generative_models
from vertexai.preview.generative_models import GenerativeModel
from django.conf import settings


class AIMatcherService:
    """Service for AI-powered resume matching using Vertex AI."""
    
    def __init__(self):
        """Initialize Vertex AI."""
        vertexai.init(
            project=settings.GCP_PROJECT_ID,
            location=settings.GCP_VERTEX_AI_LOCATION
        )
        self.model = GenerativeModel(settings.GCP_MODEL_NAME)
    
    def calculate_match_score(
        self, 
        extracted_text: str, 
        job_description: str, 
        category: str
    ) -> str:
        """
        Calculate match score between resume and job description.
        
        Args:
            extracted_text: Extracted text from resume/job description
            job_description: Job description or requirements
            category: 'resume' for resume matching, 'job_search' for job search
        
        Returns:
            Match score as string (0-1)
        """
        prompt = self._build_prompt(extracted_text, job_description, category)
        
        try:
            responses = self.model.generate_content(
                prompt,
                generation_config={
                    "max_output_tokens": 2048,
                    "temperature": 0.4,
                    "top_p": 1,
                    "top_k": 32
                },
                safety_settings={
                    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: 
                        generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: 
                        generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: 
                        generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: 
                        generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                },
                stream=True,
            )
            
            # Get first response
            for response in responses:
                score = response.text.strip()
                # Clean up the score (remove any extra text)
                try:
                    float(score)
                    return score
                except ValueError:
                    # Extract numeric value if wrapped in text
                    import re
                    match = re.search(r'0?\.\d+|1\.0|1|0', score)
                    if match:
                        return match.group()
                    return "0"
            
            return "0"
            
        except Exception as e:
            print(f"Error calculating match score: {e}")
            return "0"
    
    def _build_prompt(
        self, 
        extracted_text: str, 
        job_description: str, 
        category: str
    ) -> str:
        """
        Build appropriate prompt based on category.
        
        Args:
            extracted_text: Extracted text from document
            job_description: Job description or requirements
            category: 'resume' or 'job_search'
        
        Returns:
            Formatted prompt string
        """
        if category == "resume":
            # Matching resumes against job description
            return f"""Please assess the match between the following job description "{job_description}" 
and resume converted to string which is as follows "{extracted_text}".
Provide a probability score between 0 to 1 indicating the degree of 
match (1 being a perfect match, 0 being no match). No verbal explanation is required"""
        else:
            # Matching job descriptions against requirements
            return f"""Please assess the match between how well my requirements 
align with the provided job description. My requirements is as follows "{job_description}" 
and the job Description converted from docx to string looks like this "{extracted_text}".
Provide only the probability score between 0 to 1 indicating the degree of match 
(1 being a perfect match, 0 being no match). No verbal explanation is required"""
