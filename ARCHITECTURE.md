# Architecture Overview

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client/User                             │
│                    (HTTP Requests/Responses)                    │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Django REST API                            │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │              API Layer (apps/matcher/api/)                │ │
│  │  ┌──────────┐  ┌─────────────┐  ┌──────────────┐        │ │
│  │  │  urls.py │→ │  views.py   │→ │serializers.py│        │ │
│  │  └──────────┘  └─────────────┘  └──────────────┘        │ │
│  │       ↓              ↓                  ↓                 │ │
│  └───────┼──────────────┼──────────────────┼─────────────────┘ │
│          │              │                  │                   │
│          │              ▼                  │                   │
│  ┌───────┼──────────────────────────────┐  │                   │
│  │       │    Service Layer             │  │                   │
│  │       │  (apps/matcher/services/)    │  │                   │
│  │       │                              │  │                   │
│  │       │  ┌────────────────────────┐  │  │                   │
│  │       └─→│ matcher_service.py     │  │  │                   │
│  │          │  - process_matching()   │  │  │                   │
│  │          │  - process_files()      │  │  │                   │
│  │          │  - generate_response()  │  │  │                   │
│  │          └──────────┬──────────────┘  │  │                   │
│  └─────────────────────┼─────────────────┘  │                   │
│                        │                    │                   │
│                        ▼                    ▼                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │         Utility Layer (core/utils/)                     │   │
│  │  ┌──────────────────┐ ┌─────────────────┐ ┌──────────┐ │   │
│  │  │ gcp_storage.py   │ │document_proc.py │ │ai_match. │ │   │
│  │  │  - list_files()  │ │  - extract_text │ │py        │ │   │
│  │  │  - download()    │ │  - process_pdf  │ │ - calc_  │ │   │
│  │  └──────────────────┘ └─────────────────┘ │   score  │ │   │
│  │                                            └──────────┘ │   │
│  └─────────────────────────────────────────────────────────┘   │
│                        │                    │           │       │
└────────────────────────┼────────────────────┼───────────┼───────┘
                         │                    │           │
                         ▼                    ▼           ▼
         ┌───────────────────────────────────────────────────────┐
         │           External Services & Storage                 │
         │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐  │
         │  │   Google     │ │   Google     │ │   Google     │  │
         │  │   Cloud      │ │  Document    │ │   Vertex     │  │
         │  │   Storage    │ │     AI       │ │     AI       │  │
         │  │   (GCS)      │ │   (OCR)      │ │  (Gemini)    │  │
         │  └──────────────┘ └──────────────┘ └──────────────┘  │
         └───────────────────────────────────────────────────────┘

                         ▲
                         │
                         ▼
         ┌───────────────────────────────────────────────────────┐
         │              Database (SQLite/PostgreSQL)             │
         │  ┌──────────────┐            ┌──────────────┐         │
         │  │ ResumeData   │            │ DocumentData │         │
         │  │  - context   │            │  - filename  │         │
         │  │  - threshold │            │  - score     │         │
         │  └──────────────┘            └──────────────┘         │
         └───────────────────────────────────────────────────────┘
```

## Request Flow

### 1. Resume Matching Request Flow

```
Client Request
    │
    ├─→ POST /api/match/
    │   {
    │     "context": "Job Description",
    │     "category": "resume",
    │     "threshold": "0.7",
    │     "noOfMatches": 5,
    │     "inputPath": "gs://bucket"
    │   }
    │
    ▼
API Layer (views.py)
    │
    ├─→ Validate request (serializers.py)
    │   └─→ Check required fields
    │       └─→ Validate threshold (0-1)
    │           └─→ Validate category
    │
    ├─→ Save request to database
    │
    ▼
Service Layer (matcher_service.py)
    │
    ├─→ Generate unique ID for request
    │
    ├─→ Process files from GCS bucket
    │   │
    │   ├─→ GCPStorageHandler.list_files()
    │   │   └─→ Get all PDFs/DOCX from bucket
    │   │
    │   ├─→ For each file:
    │   │   │
    │   │   ├─→ DocumentProcessor.extract_text()
    │   │   │   └─→ PDF: Use Document AI OCR
    │   │   │   └─→ DOCX: Use docx2txt
    │   │   │
    │   │   ├─→ AIMatcherService.calculate_score()
    │   │   │   └─→ Send to Vertex AI Gemini
    │   │   │   └─→ Get confidence score (0-1)
    │   │   │
    │   │   └─→ Store in database
    │   │       └─→ DocumentData.create()
    │   │
    │   └─→ Continue for all files
    │
    ├─→ Query database for results
    │   └─→ Filter by: unique_id + threshold
    │       └─→ Order by: score (descending)
    │           └─→ Limit: noOfMatches
    │
    ▼
Response to Client
    {
      "count": 3,
      "metadata": {"confidenceScore": 0.7},
      "results": [
        {"id": "resume1.pdf", "path": "...", "score": "0.95"},
        {"id": "resume2.pdf", "path": "...", "score": "0.87"}
      ],
      "status": "success"
    }
```

## Layer Responsibilities

### API Layer (`apps/matcher/api/`)
**Purpose**: Handle HTTP requests and responses
- Receive and validate incoming requests
- Serialize/deserialize data
- Handle HTTP status codes
- Format responses
- Route requests to appropriate handlers

### Service Layer (`apps/matcher/services/`)
**Purpose**: Implement business logic
- Orchestrate operations across utilities
- Process resume matching workflow
- Generate unique identifiers
- Coordinate file processing
- Query and format results
- Handle business exceptions

### Utility Layer (`core/utils/`)
**Purpose**: Provide reusable functionality
- **GCPStorageHandler**: GCS operations
- **DocumentProcessor**: Text extraction
- **AIMatcherService**: AI matching

### Data Layer (`apps/matcher/models.py`)
**Purpose**: Data persistence
- Define database schema
- Provide data access interface
- Handle data validation
- Manage relationships

## Technology Stack Flow

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │ HTTP/REST
       ▼
┌─────────────────────┐
│ Django REST Framework│
└──────┬──────────────┘
       │
       ├─→ Django ORM ──→ SQLite/PostgreSQL
       │
       ├─→ Google Cloud Storage
       │
       ├─→ Google Document AI (OCR)
       │
       └─→ Google Vertex AI (Gemini)
```

## Deployment Architecture

```
┌─────────────────────────────────────────┐
│        Google Cloud Run                 │
│                                         │
│  ┌───────────────────────────────────┐  │
│  │     Docker Container              │  │
│  │  ┌─────────────────────────────┐  │  │
│  │  │   Gunicorn (WSGI Server)    │  │  │
│  │  │  ┌───────────────────────┐  │  │  │
│  │  │  │   Django Application  │  │  │  │
│  │  │  └───────────────────────┘  │  │  │
│  │  └─────────────────────────────┘  │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
           │
           ├─→ Google Artifact Registry (Images)
           ├─→ Google Cloud Storage (Files)
           ├─→ Google Document AI (OCR)
           └─→ Google Vertex AI (Matching)
```

## Key Design Principles

1. **Separation of Concerns**: Each layer has distinct responsibilities
2. **Single Responsibility**: Each module/class has one clear purpose
3. **Dependency Injection**: Services receive dependencies, not create them
4. **Loose Coupling**: Layers interact through clean interfaces
5. **High Cohesion**: Related functionality grouped together
6. **Testability**: Isolated layers are easy to test
7. **Scalability**: Modular design allows horizontal scaling
8. **Maintainability**: Clear structure makes updates easier

## Security Architecture

```
Environment Variables (.env)
    │
    ├─→ DJANGO_SECRET_KEY (Django security)
    ├─→ GCP_PROJECT_ID (GCP access)
    ├─→ GOOGLE_APPLICATION_CREDENTIALS (Auth)
    └─→ DEBUG (Environment control)

Service Account (creds.json)
    │
    ├─→ Document AI User (OCR access)
    ├─→ Vertex AI User (AI access)
    └─→ Storage Object Viewer (Read GCS)

Django Security Middleware
    │
    ├─→ CSRF Protection
    ├─→ XSS Protection
    ├─→ SSL Redirect (Production)
    └─→ Security Headers
```
