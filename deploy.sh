#!/bin/bash

# Gmail MCP Server Cloud Run Deployment Script
# This script automates the deployment process to Google Cloud Run

set -e  # Exit on any error

# Configuration
PROJECT_ID=${PROJECT_ID:-"your-project-id"}
SERVICE_NAME="gmail-mcp-server"
REGION="us-central1"
IMAGE_NAME="gcr.io/$PROJECT_ID/$SERVICE_NAME"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Helper functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check if gcloud is installed
    if ! command -v gcloud &> /dev/null; then
        log_error "gcloud CLI is not installed. Please install it first."
        exit 1
    fi
    
    # Check if docker is installed
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed. Please install it first."
        exit 1
    fi
    
    # Check if PROJECT_ID is set
    if [ "$PROJECT_ID" = "your-project-id" ]; then
        log_error "Please set PROJECT_ID environment variable or update the script."
        exit 1
    fi
    
    log_info "Prerequisites check passed!"
}

# Set up Google Cloud project
setup_project() {
    log_info "Setting up Google Cloud project..."
    
    # Set the project
    gcloud config set project $PROJECT_ID
    
    # Enable required APIs
    log_info "Enabling required APIs..."
    gcloud services enable run.googleapis.com
    gcloud services enable gmail.googleapis.com
    gcloud services enable cloudbuild.googleapis.com
    gcloud services enable containerregistry.googleapis.com
    
    log_info "Project setup completed!"
}

# Create service account
create_service_account() {
    log_info "Creating service account..."
    
    # Check if service account already exists
    if gcloud iam service-accounts describe gmail-mcp-server@$PROJECT_ID.iam.gserviceaccount.com &> /dev/null; then
        log_warn "Service account already exists, skipping creation."
    else
        # Create service account
        gcloud iam service-accounts create gmail-mcp-server \
            --display-name="Gmail MCP Server" \
            --description="Service account for Gmail MCP Server"
        
        log_info "Service account created successfully!"
    fi
    
    # Grant necessary permissions
    log_info "Granting permissions..."
    gcloud projects add-iam-policy-binding $PROJECT_ID \
        --member="serviceAccount:gmail-mcp-server@$PROJECT_ID.iam.gserviceaccount.com" \
        --role="roles/gmail.readonly" \
        --quiet || true
    
    gcloud projects add-iam-policy-binding $PROJECT_ID \
        --member="serviceAccount:gmail-mcp-server@$PROJECT_ID.iam.gserviceaccount.com" \
        --role="roles/gmail.send" \
        --quiet || true
    
    log_info "Permissions granted!"
}

# Create credentials file
create_credentials() {
    log_info "Creating credentials file..."
    
    if [ -f "credentials.json" ]; then
        log_warn "credentials.json already exists, skipping creation."
    else
        # Create and download service account key
        gcloud iam service-accounts keys create credentials.json \
            --iam-account=gmail-mcp-server@$PROJECT_ID.iam.gserviceaccount.com
        
        log_info "Credentials file created successfully!"
    fi
}

# Build and push Docker image
build_and_push() {
    log_info "Building and pushing Docker image..."
    
    # Build the image
    log_info "Building Docker image..."
    docker build -t $IMAGE_NAME:latest .
    
    # Configure Docker to use gcloud as a credential helper
    gcloud auth configure-docker
    
    # Push the image
    log_info "Pushing Docker image..."
    docker push $IMAGE_NAME:latest
    
    log_info "Docker image built and pushed successfully!"
}

# Deploy to Cloud Run
deploy_to_cloud_run() {
    log_info "Deploying to Cloud Run..."
    
    # Deploy the service
    gcloud run deploy $SERVICE_NAME \
        --image $IMAGE_NAME:latest \
        --platform managed \
        --region $REGION \
        --allow-unauthenticated \
        --memory 512Mi \
        --cpu 1 \
        --max-instances 10 \
        --min-instances 0 \
        --timeout 300 \
        --concurrency 80 \
        --set-env-vars \
        GMAIL_CREDENTIALS_FILE=/app/credentials.json,\
        GMAIL_TOKEN_FILE=/tmp/token.json,\
        MCP_SERVER_NAME=gmail-mcp-server,\
        MCP_SERVER_VERSION=1.0.0,\
        DEFAULT_MAX_RESULTS=50,\
        DEFAULT_QUERY=in:inbox,\
        LOG_LEVEL=INFO
    
    log_info "Deployment completed successfully!"
}

# Get service URL
get_service_url() {
    log_info "Getting service URL..."
    
    SERVICE_URL=$(gcloud run services describe $SERVICE_NAME \
        --region $REGION \
        --format 'value(status.url)')
    
    log_info "Service URL: $SERVICE_URL"
    echo "Service URL: $SERVICE_URL" > service_url.txt
}

# Test the deployment
test_deployment() {
    log_info "Testing deployment..."
    
    if [ -n "$SERVICE_URL" ]; then
        # Test the service
        log_info "Testing service health..."
        curl -f "$SERVICE_URL" || log_warn "Service health check failed, but deployment may still be successful."
    else
        log_warn "Service URL not available for testing."
    fi
}

# Clean up
cleanup() {
    log_info "Cleaning up..."
    
    # Remove credentials file for security
    if [ -f "credentials.json" ]; then
        rm credentials.json
        log_info "Credentials file removed for security."
    fi
}

# Main deployment function
main() {
    log_info "Starting Gmail MCP Server deployment to Cloud Run..."
    
    check_prerequisites
    setup_project
    create_service_account
    create_credentials
    build_and_push
    deploy_to_cloud_run
    get_service_url
    test_deployment
    
    log_info "Deployment completed successfully!"
    log_info "Your Gmail MCP Server is now running on Cloud Run."
    log_info "Service URL: $SERVICE_URL"
    
    # Ask if user wants to clean up credentials
    read -p "Do you want to remove the credentials file for security? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cleanup
    fi
}

# Run main function
main "$@"
