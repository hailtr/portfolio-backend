# PDF Generation Microservice

A lightweight microservice for generating PDFs using WeasyPrint, designed to run on Google Cloud Run.

## Deployment to GCP Cloud Run

### Prerequisites
- Google Cloud CLI installed (`gcloud`)
- A GCP project with Cloud Run enabled

### Deploy Steps

1. **Authenticate with GCP:**
```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

2. **Enable required APIs:**
```bash
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

3. **Build and deploy:**
```bash
cd pdf-service

# Build and push to Container Registry
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/pdf-service

# Deploy to Cloud Run (2GB memory for WeasyPrint)
gcloud run deploy pdf-service \
  --image gcr.io/YOUR_PROJECT_ID/pdf-service \
  --platform managed \
  --region us-central1 \
  --memory 2Gi \
  --timeout 120 \
  --concurrency 10 \
  --allow-unauthenticated
```

4. **Get the service URL:**
```bash
gcloud run services describe pdf-service --region us-central1 --format="value(status.url)"
```

5. **Set the URL in your main backend:**
Add to Render environment variables:
```
PDF_SERVICE_URL=https://pdf-service-xxxxx-uc.a.run.app
```

## API Endpoints

### Health Check
```
GET /health
```

### Generate PDF from HTML
```
POST /generate
Content-Type: application/json

{
    "html_content": "<html>...</html>",
    "css_content": "...",  // Optional
    "lang": "en"
}
```

Returns: PDF file (application/pdf)

## Local Testing

```bash
# Build
docker build -t pdf-service .

# Run
docker run -p 8080:8080 pdf-service

# Test
curl -X POST http://localhost:8080/generate \
  -H "Content-Type: application/json" \
  -d '{"html_content": "<html><body><h1>Test</h1></body></html>", "lang": "en"}' \
  --output test.pdf
```
