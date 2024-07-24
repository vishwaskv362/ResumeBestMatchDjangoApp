import io

from google.cloud import documentai_v1 as documentai


# import logging


# logging.basicConfig(filename='document_processing.log', level=logging.ERROR)
# logger = logging.getLogger(__name__)


def process_document(project_id, location, processor_id, file_path):
    """Processes a document using the Document AI API."""

    client = documentai.DocumentProcessorServiceClient()
    name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"

    try:
        image_file = io.BytesIO()
        file_path.download_to_file(image_file)

        raw_document = documentai.RawDocument(content=image_file.getvalue(),
                                              mime_type="application/pdf")

        request = documentai.ProcessRequest(name=name, raw_document=raw_document)
        result = client.process_document(request=request)

        document = result.document
        text = document.text
        return text

    except Exception as e:
        print(f"Error processing {file_path.name}: {e}")
        return "None"
