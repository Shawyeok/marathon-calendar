#!/bin/bash
#
# Manual R2 Upload Script
# This script allows you to manually upload ICS files to Cloudflare R2
# Useful for testing or manual deployments
#
# Usage:
#   ./scripts/upload_to_r2.sh
#
# Prerequisites:
#   - AWS CLI installed (pip install awscli)
#   - Environment variables set:
#     - R2_ACCOUNT_ID
#     - R2_BUCKET_NAME
#     - AWS_ACCESS_KEY_ID (R2 Access Key)
#     - AWS_SECRET_ACCESS_KEY (R2 Secret Key)
#

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored messages
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    print_error "AWS CLI is not installed. Install it with: pip install awscli"
    exit 1
fi

# Check required environment variables
if [ -z "$R2_ACCOUNT_ID" ]; then
    print_error "R2_ACCOUNT_ID environment variable is not set"
    exit 1
fi

if [ -z "$R2_BUCKET_NAME" ]; then
    print_error "R2_BUCKET_NAME environment variable is not set"
    exit 1
fi

if [ -z "$AWS_ACCESS_KEY_ID" ]; then
    print_error "AWS_ACCESS_KEY_ID environment variable is not set"
    exit 1
fi

if [ -z "$AWS_SECRET_ACCESS_KEY" ]; then
    print_error "AWS_SECRET_ACCESS_KEY environment variable is not set"
    exit 1
fi

# Configuration
R2_ENDPOINT="https://${R2_ACCOUNT_ID}.r2.cloudflarestorage.com"
OUTPUT_DIR="output"

print_info "Starting R2 upload..."
print_info "Endpoint: ${R2_ENDPOINT}"
print_info "Bucket: ${R2_BUCKET_NAME}"
echo ""

# Check if output directory exists
if [ ! -d "$OUTPUT_DIR" ]; then
    print_error "Output directory '$OUTPUT_DIR' does not exist"
    print_info "Please run: python scripts/generate_calendar.py"
    exit 1
fi

# Count ICS files
ICS_FILES=("$OUTPUT_DIR"/*.ics)
if [ ! -f "${ICS_FILES[0]}" ]; then
    print_error "No .ics files found in $OUTPUT_DIR"
    print_info "Please run: python scripts/generate_calendar.py"
    exit 1
fi

# Upload each ICS file
UPLOADED=0
FAILED=0

for filepath in "$OUTPUT_DIR"/*.ics; do
    if [ -f "$filepath" ]; then
        filename=$(basename "$filepath")
        filesize=$(du -h "$filepath" | cut -f1)
        
        print_info "Uploading: $filename ($filesize)"
        
        if aws s3 cp "$filepath" "s3://${R2_BUCKET_NAME}/$filename" \
            --endpoint-url "$R2_ENDPOINT" \
            --content-type "text/calendar" \
            --cache-control "max-age=3600" \
            --metadata "generated=$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
            2>&1 | grep -q "upload:"; then
            
            print_success "Uploaded: $filename"
            ((UPLOADED++))
        else
            print_error "Failed to upload: $filename"
            ((FAILED++))
        fi
    fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ $FAILED -eq 0 ]; then
    print_success "All files uploaded successfully! ($UPLOADED files)"
else
    print_warning "Upload completed with errors"
    print_info "Uploaded: $UPLOADED"
    print_error "Failed: $FAILED"
fi
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# List uploaded files (optional)
if [ $UPLOADED -gt 0 ]; then
    echo ""
    print_info "Listing files in R2 bucket:"
    aws s3 ls "s3://${R2_BUCKET_NAME}/" --endpoint-url "$R2_ENDPOINT" | grep ".ics"
fi

exit 0

