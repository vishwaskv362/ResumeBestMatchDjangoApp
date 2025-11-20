# AI Resume Hunter

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/Django-4.2+-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A production-ready Django REST API that intelligently matches resumes against job descriptions using Google Cloud AI services. The application leverages Document AI for OCR text extraction and Vertex AI (Gemini) for advanced semantic matching.

## 🚀 Features

- **Intelligent Resume Matching**: AI-powered matching using Google Vertex AI (Gemini)
- **Multi-Format Support**: Process PDF and DOCX files automatically
- **OCR Integration**: Extract text from documents using Google Document AI
- **Flexible Matching**: Support for both resume-to-job and job-to-requirement matching
- **RESTful API**: Clean, well-documented API endpoints
- **Cloud Storage Integration**: Direct integration with Google Cloud Storage
- **Dockerized**: Production-ready containerization with Docker Compose
- **Scalable Architecture**: Modular design with separated concerns

## 🏗️ Architecture

```
AIResumeHunter/
├── config/                      # Project configuration
│   ├── settings/               # Split settings (base, production)
│   ├── urls.py                 # Main URL configuration
│   ├── wsgi.py                 # WSGI config
│   └── asgi.py                 # ASGI config
├── apps/                        # Django applications
│   └── matcher/                # Resume matching app
│       ├── api/                # API layer
│       │   ├── serializers.py  # Request/Response serializers
│       │   ├── views.py        # API views
│       │   └── urls.py         # API routes
│       ├── services/           # Business logic layer
│       │   └── matcher_service.py
│       ├── models.py           # Database models
│       └── admin.py            # Admin interface
├── core/                        # Core utilities
│   └── utils/                  # Helper utilities
│       ├── gcp_storage.py      # GCS operations
│       ├── document_processor.py  # Document text extraction
│       └── ai_matcher.py       # AI matching logic
├── manage.py                    # Django management
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker configuration
└── docker-compose.yml          # Docker Compose setup
```

## 🛠️ Tech Stack

### Backend Framework
- **Django 4.2+**: High-level Python web framework
- **Django REST Framework**: Toolkit for building Web APIs

### AI & Machine Learning
- **Google Vertex AI**: Gemini AI model for intelligent matching
- **Google Document AI**: OCR and document processing

### Cloud Services
- **Google Cloud Storage**: Document storage and retrieval
- **Google Cloud Run**: Serverless deployment platform
- **Google Artifact Registry**: Container image storage

### Document Processing
- **docx2txt**: DOCX file text extraction
- **Google Document AI**: PDF text extraction with OCR

### Infrastructure
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **Gunicorn**: WSGI HTTP Server for production

### Development Tools
- **pytest**: Testing framework
- **black**: Code formatter
- **flake8**: Code linter

## 📋 Prerequisites

- Python 3.11+
- Docker and Docker Compose
- Google Cloud Platform account with:
  - Document AI API enabled
  - Vertex AI API enabled
  - Cloud Storage bucket created
- GCP service account credentials

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/vishwaskv362/ResumeBestMatchDjangoApp.git
cd AIResumeHunter
```

### 2. Google Cloud Setup

1. **Create a GCP project**

2. **Enable required APIs:**
   - Document AI API
   - Vertex AI API
   - Cloud Storage API

3. **Create a service account with roles:**
   - Document AI User
   - Vertex AI User
   - Storage Object Viewer

4. **Download service account key** and save as `application_default_credentials.json` or `creds.json` in the project root

5. **Create a Cloud Storage bucket** for resumes

### 3. Set Up Environment Variables

Copy the environment template and fill in your values:

```bash
cp .env.example .env
```

Edit `.env`:

```bash
# Django Settings
DJANGO_SECRET_KEY=your-secret-key-here  # Generate: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
DEBUG=True
DJANGO_ENV=development
ALLOWED_HOSTS=localhost,127.0.0.1

# Google Cloud Settings
GCP_PROJECT_ID=your-project-id
GCP_LOCATION=us
GCP_PROCESSOR_ID=your-processor-id
GCP_VERTEX_AI_LOCATION=us-central1
GCP_MODEL_NAME=gemini-1.0-pro-vision-001
GOOGLE_APPLICATION_CREDENTIALS=application_default_credentials.json
```

### 4. Install Dependencies

#### Using Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 5. Run Migrations

```bash
python manage.py migrate
```

### 6. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 7. Run Development Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000`

## 🐳 Docker Deployment

### Build and Run with Docker Compose

```bash
# Build and run
docker-compose up --build

# Run in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop containers
docker-compose down
```

The API will be available at `http://localhost:8000`

### Production Deployment

```bash
docker build -t resume-matcher-api .
docker run -p 8000:8000 --env-file .env resume-matcher-api
```

## 🧪 Testing the API

### Health Check
```bash
curl http://localhost:8000/api/health/
```

### Test Matching
```bash
curl -X POST http://localhost:8000/api/match/ \
  -H "Content-Type: application/json" \
  -d '{
    "context": "Looking for Python developer with Django experience",
    "category": "resume",
    "threshold": "0.7",
    "noOfMatches": 5,
    "inputPath": "gs://your-bucket-name"
  }'
```

## 📡 API Endpoints

### Health Check
```http
GET /api/health/
```

**Response:**
```json
{
  "status": "healthy",
  "message": "AI Resume Hunter API is running"
}
```

### Resume Matching
```http
POST /api/match/
Content-Type: application/json
```

**Request Body:**
```json
{
  "context": "Looking for a senior Python developer with Django experience...",
  "category": "resume",
  "threshold": "0.7",
  "noOfMatches": 5,
  "inputPath": "gs://your-bucket-name"
}
```

**Parameters:**
- `context` (string): Job description or requirements
- `category` (string): Either "resume" (match resumes to job) or "job_search" (match jobs to requirements)
- `threshold` (string): Minimum confidence score (0-1)
- `noOfMatches` (integer): Number of top matches to return
- `inputPath` (string): GCS bucket path containing resumes

**Response:**
```json
{
  "count": 3,
  "metadata": {
    "confidenceScore": 0.7
  },
  "results": [
    {
      "id": "resume_1.pdf",
      "path": "https://storage.googleapis.com/bucket/resume_1.pdf",
      "score": "0.95"
    },
    {
      "id": "resume_2.pdf",
      "path": "https://storage.googleapis.com/bucket/resume_2.pdf",
      "score": "0.87"
    }
  ],
  "status": "success"
}
```

### Statistics
```http
GET /api/stats/
```

**Response:**
```json
{
  "total_requests": 42,
  "status": "success"
}
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DJANGO_SECRET_KEY` | Django secret key | (generated) |
| `DEBUG` | Debug mode | `True` |
| `DJANGO_ENV` | Environment (development/production) | `development` |
| `ALLOWED_HOSTS` | Allowed host domains | `*` |
| `GCP_PROJECT_ID` | Google Cloud project ID | Required |
| `GCP_LOCATION` | Document AI location | `us` |
| `GCP_PROCESSOR_ID` | Document AI processor ID | Required |
| `GCP_VERTEX_AI_LOCATION` | Vertex AI location | `us-central1` |
| `GCP_MODEL_NAME` | Gemini model name | `gemini-1.0-pro-vision-001` |

## 🧪 Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=apps --cov=core

# Run specific test file
pytest apps/matcher/tests/test_api.py
```

## 🔧 Troubleshooting

### Import Errors
- Make sure you're in the project root directory
- Activate virtual environment: `source venv/bin/activate` (Windows: `venv\Scripts\activate`)
- Check PYTHONPATH includes the project root

### GCP Authentication Issues
- Verify credentials file path in `.env`
- Check service account has required permissions
- Ensure APIs are enabled in GCP console
- Test credentials: `gcloud auth application-default print-access-token`

### Docker Issues
- Ensure credentials files are in the project root
- Check docker-compose.yml volume mappings
- Verify port 8000 is available: `netstat -an | findstr 8000`
- Clean rebuild: `docker-compose down -v && docker-compose build --no-cache`

## 📊 Database Models

### ResumeData
Stores incoming matching requests with job descriptions and parameters.

### DocumentData
Stores extracted text and confidence scores for each processed document.

## 🔐 Security Considerations

- Store GCP credentials securely (use Secret Manager in production)
- Use environment variables for sensitive configuration
- Enable HTTPS in production
- Implement rate limiting for API endpoints
- Regularly update dependencies

## 🚀 Deployment

### Google Cloud Run

1. Build and push Docker image:
```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/resume-matcher-api
```

2. Deploy to Cloud Run:
```bash
gcloud run deploy resume-matcher-api \
  --image gcr.io/PROJECT_ID/resume-matcher-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## 📝 License

This project is licensed under the MIT License.

## 👤 Author

**Vishwakarma KV**
- GitHub: [@vishwaskv362](https://github.com/vishwaskv362)

## 🙏 Acknowledgments

- Google Cloud AI services for powerful ML capabilities
- Django and DRF communities for excellent frameworks
- Open source contributors

## 📸 Screenshots

![App Screenshot](https://github.com/user-attachments/assets/284bb4a3-757a-454a-9a13-e3e6ef33efb4)

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

## ⭐ Show your support

Give a ⭐️ if this project helped you!

