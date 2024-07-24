import vertexai
import vertexai.preview.generative_models as generative_models
from vertexai.preview.generative_models import GenerativeModel


def generate(extracted_text, job_description, category):
    print(f"+++++++++++++++++++++++ Category is {category} +++++++++++++++++++++++")
    vertexai.init(project="wellsfargo-genai24-8032", location="us-central1")
    model = GenerativeModel("gemini-1.0-pro-vision-001")

    # Assuming i am recruiter and i have 100's of resumes to be filtered for a specific job position, we can use this API
    prompt_for_resume = f"""Please assess the match between the following job description \"{job_description}\" 
    and resume converted to string which is as follows \"{extracted_text}\".
    Provide a probability score between 0 to 1 indicating the degree of 
    match (1 being a perfect match, 0 being no match).No verbal explanation is required"""

    # Assuming i am a person who is looking for the internal job change with the job _requirements, we can get the matching JOB ID based on the  Description provided
    prompt_for_job_search = f"""Please assess the match between how well my requirements 
    align with the provided job description. My requirements is as follows \"{job_description}\" and the job Description 
    converted from docx to string looks like this  \"{extracted_text}\".Provide only the probability 
    score between 0 to 1 indicating the degree of match (1 being a perfect match, 0 being no match).
    No verbal explanation is required"""

    # We even have a healthcheck API, which just checks whether the Application is alive or not

    if category == "resume":
        prompt = prompt_for_resume
    else:
        prompt = prompt_for_job_search
    responses = model.generate_content(
        prompt,
        generation_config={
            "max_output_tokens": 2048,
            "temperature": 0.4,
            "top_p": 1,
            "top_k": 32
        },
        safety_settings={
            generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        },
        stream=True,
    )

    for response in responses:
        return response.text
