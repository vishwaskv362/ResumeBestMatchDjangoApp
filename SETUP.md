# Setup Guide

## Quick Setup Steps

### 1. Environment Setup

1. Copy the environment template:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and fill in your values:
   - `DJANGO_SECRET_KEY`: Generate using `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
   - `GCP_PROJECT_ID`: Your Google Cloud project ID
   - `GCP_PROCESSOR_ID`: Your Document AI processor ID

### 2. Google Cloud Setup

1. Create a GCP project
2. Enable required APIs:
   - Document AI API
   - Vertex AI API
   - Cloud Storage API

3. Create a service account with roles:
   - Document AI User
   - Vertex AI User
   - Storage Object Viewer

4. Download service account key and save as `application_default_credentials.json` or `creds.json`

5. Create a Cloud Storage bucket for resumes

### 3. Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### 4. Docker Setup

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

### 5. Testing the API

```bash
# Health check
curl http://localhost:8000/api/health/

# Test matching (replace with your bucket and job description)
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

## Troubleshooting

### Import Errors
- Make sure you're in the project root directory
- Activate virtual environment
- Check PYTHONPATH includes the project root

### GCP Authentication
- Verify credentials file path in `.env`
- Check service account has required permissions
- Ensure APIs are enabled in GCP console

### Docker Issues
- Ensure credentials files are in the project root
- Check docker-compose.yml volume mappings
- Verify port 8000 is available

## Production Deployment

See README.md for detailed production deployment instructions.
