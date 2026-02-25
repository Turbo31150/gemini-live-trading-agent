#!/bin/bash
# Cleanup Cloud Run deployment
# Usage: ./deploy/cleanup.sh [PROJECT_ID] [REGION]

set -euo pipefail

PROJECT_ID="${1:-$(gcloud config get-value project)}"
REGION="${2:-us-central1}"
SERVICE_NAME="gemini-live-trading-agent"

echo "=== Cleaning up ${SERVICE_NAME} ==="

# Delete Cloud Run service
gcloud run services delete "${SERVICE_NAME}" \
    --region="${REGION}" \
    --project="${PROJECT_ID}" \
    --quiet || echo "Service not found, skipping..."

# Delete container image
gcloud container images delete "gcr.io/${PROJECT_ID}/${SERVICE_NAME}" \
    --force-delete-tags \
    --quiet || echo "Image not found, skipping..."

echo "Cleanup complete."
