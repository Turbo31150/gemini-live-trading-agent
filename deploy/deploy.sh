#!/bin/bash
# Automated Cloud Run deployment for Gemini Live Trading Agent
# Usage: ./deploy/deploy.sh [PROJECT_ID] [REGION]

set -euo pipefail

PROJECT_ID="${1:-$(gcloud config get-value project)}"
REGION="${2:-us-central1}"
SERVICE_NAME="gemini-live-trading-agent"
IMAGE="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

echo "=== Gemini Live Trading Agent — Cloud Run Deployment ==="
echo "Project:  ${PROJECT_ID}"
echo "Region:   ${REGION}"
echo "Service:  ${SERVICE_NAME}"
echo ""

# 1. Enable required APIs
echo "[1/5] Enabling Google Cloud APIs..."
gcloud services enable \
    run.googleapis.com \
    aiplatform.googleapis.com \
    containerregistry.googleapis.com \
    cloudbuild.googleapis.com \
    --project="${PROJECT_ID}" --quiet

# 2. Build container image
echo "[2/5] Building container image..."
gcloud builds submit \
    --tag "${IMAGE}" \
    --project="${PROJECT_ID}" \
    --quiet

# 3. Deploy to Cloud Run
echo "[3/5] Deploying to Cloud Run..."
gcloud run deploy "${SERVICE_NAME}" \
    --image "${IMAGE}" \
    --region "${REGION}" \
    --project="${PROJECT_ID}" \
    --platform managed \
    --allow-unauthenticated \
    --set-env-vars "PROJECT_ID=${PROJECT_ID},LOCATION=${REGION},MODEL=gemini-live-2.5-flash-native-audio" \
    --memory 512Mi \
    --cpu 1 \
    --timeout 600 \
    --max-instances 10 \
    --min-instances 0 \
    --session-affinity \
    --quiet

# 4. Get service URL
echo "[4/5] Retrieving service URL..."
SERVICE_URL=$(gcloud run services describe "${SERVICE_NAME}" \
    --region="${REGION}" \
    --project="${PROJECT_ID}" \
    --format="value(status.url)")

echo ""
echo "[5/5] Deployment complete!"
echo "=========================================="
echo "Service URL: ${SERVICE_URL}"
echo "Health:      ${SERVICE_URL}/api/health"
echo "=========================================="
echo ""
echo "Test with: curl ${SERVICE_URL}/api/health"
